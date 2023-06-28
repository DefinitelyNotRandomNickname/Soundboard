import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

import pygame
import pygame._sdl2.audio as sdl2_audio
from pydub import AudioSegment
import keyboard
import os

device = None

play_handler = None
play_button = None

volume = None
db = None

audio_folder = 'tracks'
track = None


def refresh_list(item_list):
    # Get the list of items from the folder
    folder = 'tracks'  # Replace with the actual folder path
    items = os.listdir(folder)

    # Clear the existing list
    item_list.delete(0, tk.END)

    # Populate the listbox with the new items
    for item in items:
        item_list.insert(tk.END, item)


def change_track(event):
    global track

    widget = event.widget
    track = widget.get(widget.curselection())


def update_volume_label(value):
    global volume
    new_value = float(value)
    volume.set(int(new_value))
    pygame.mixer.music.set_volume(new_value / 100)


def update_db_label(value):
    global db
    db.set(int(float(value)))


def play():
    global track
    global dB
    global device

    if not pygame.mixer.music.get_busy() and track:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        # Clear folder
        for filename in os.listdir("tmp"):
            file_path = os.path.join("tmp", filename)
            if os.path.isfile(file_path):
                # Remove the file
                os.remove(file_path)

        # Load the audio file using pydub
        audio = audio_folder + '/' + track
        audio_file = AudioSegment.from_file(audio)

        # Increase the volume by a certain dB level
        audio_db = audio_file + db.get()

        # Export the modified audio to a temporary file
        temp_file = "tmp" + '/' + track
        audio_db.export(temp_file, format="mp3")

        pygame.mixer.quit()
        pygame.mixer.init(devicename=device)
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()


def play_keys(event):
    global play_button
    global play_handler

    play_button = event.widget.get()
    keyboard.remove_hotkey(play_handler)
    play_handler = keyboard.add_hotkey(play_button, play)


def init_buttons():
    # Create a frame to hold the list
    frame = ttk.Frame(root, padding=10)
    frame.grid(row=1, column=0, sticky="nsew")

    # Create a scrollbar for the listbox
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a listbox to display the items
    item_list = tk.Listbox(frame, yscrollcommand=scrollbar.set)
    item_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configure the scrollbar
    scrollbar.config(command=item_list.yview)

    # Bind the <<ListboxSelect>> event to the on_item_selected function
    item_list.bind("<<ListboxSelect>>", change_track)

    # Call the refresh_list function initially to populate the list
    refresh_list(item_list)

    # Create a refresh button
    icon_image = tk.PhotoImage(file="Refresh_icon.png")

    refresh_button = ttk.Button(root, image=icon_image, command=lambda: refresh_list(item_list))
    refresh_button.image = icon_image
    refresh_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    # Create a frame for extended volume slider, and loopback checkbox
    controls_frame = ttk.Frame(root, padding=10)
    controls_frame.grid(row=1, column=1, pady=0, sticky="nsew")

    # Create a list of selected keys
    selected_key_label = ttk.Label(controls_frame, text="Play Key:")
    selected_key_label.grid(row=1, column=0, pady=10, sticky="w")

    # Create a dropdown checkbox for key selection
    key_dropdown = ttk.Combobox(controls_frame, state="readonly")
    key_dropdown['values'] = ('F9', 'F10', 'F11', 'F12')
    key_dropdown.grid(row=1, column=1, pady=10, sticky="w")
    key_dropdown.current(3)

    global play_button
    play_button = "F12"

    # Bind the <<ComboboxSelected>> event to the custom function
    key_dropdown.bind("<<ComboboxSelected>>", play_keys)

    # Create a volume label
    volume_label = ttk.Label(controls_frame, text="Volume:")
    volume_label.grid(row=4, column=0, pady=10, sticky="w")

    global volume
    volume = tk.IntVar(value=50)

    # Create a volume slider
    volume_slider = ttk.Scale(controls_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=volume,
                              command=update_volume_label)
    volume_slider.grid(row=5, column=0, pady=5, sticky="we")

    # Create a volume value label
    volume_display_label = ttk.Label(controls_frame, textvariable=volume)
    volume_display_label.grid(row=5, column=1, pady=5, sticky="w")

    # Create a dB label
    db_label = ttk.Label(controls_frame, text="dB:")
    db_label.grid(row=6, column=0, pady=10, sticky="w")

    global db
    db = tk.IntVar(value=0)

    # Create a volume slider
    db_slider = ttk.Scale(controls_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=db,
                              command=update_db_label)
    db_slider.grid(row=7, column=0, pady=5, sticky="we")

    # Create a volume value label
    db_display_label = ttk.Label(controls_frame, textvariable=db)
    db_display_label.grid(row=7, column=1, pady=5, sticky="w")

    # Configure row and column weights
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.columnconfigure(1, weight=0)
    root.rowconfigure(1, weight=1)


if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()

    root.tk.call("source", "theme.tcl")
    root.tk.call("set_theme", "dark")

    root.title("Soundboard")
    root.minsize(600, 500)  # Set minimum size

    play_button = None
    track = None

    init_buttons()

    db_folder = "tmp"

    # Check if the folder already exists
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    pygame.mixer.init()
    devices = tuple(sdl2_audio.get_audio_device_names())

    vb_audio_devices = [device for device in devices if device.startswith('CABLE Input')]
    if len(vb_audio_devices) > 0:
        device = vb_audio_devices[0]  # Select the first device
        pygame.mixer.music.set_volume(volume.get() / 100)
        play_handler = keyboard.add_hotkey(play_button, play)
    else:
        print("No matching devices found.")
        pygame.mixer.quit()

    # Start the Tkinter event loop
    root.mainloop()
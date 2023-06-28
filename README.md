# Soundboard
## Description:
The Soundboard is a Python script that allows you to play audio files through specific output devices, change their volume, and adjust the decibel level.

Please note that this script requires certain libraries listed in the `requirements.txt` file. You can install them by running the command `pip install -r requirements.txt`. Additionally, you will need to download [VB-Cable](https://vb-audio.com/Cable/) for the best use of this program and [FFmpeg](https://ffmpeg.org/download.html) to increase dB.

If you wanna hear sounds that you are streaming to VB cable go to the `Sound -> Recording -> CABLE Output -> Properties -> Listen` and check `Listen to this device`.

![](https://github.com/DefinitelyNotRandomNickname/Soundboard/blob/main/rd_prp.png)

It's important to mention that this program has only been tested on Windows. While it may not be compatible with Linux or Mac operating systems, you can still give it a try.

## Importing files
To import audio files, simply place them in the `tracks/` folder and refresh the application. Supported file formats include `.mp3` and `.wav`.

## In app
To play a track, follow these steps:

1. Select a track from the list.
2. Press the assigned key to play the selected track (default key is `F12`).

# Simple Song Display
100% human code, no LLMs.

![image](/images/showcase.png)

## ⚠️ WARNING: THIS IS JUST MADE FOR MY PERSONAL USE

Simple Song Display is a song display for a Raspberry Pi (or any* Linux machine) which receives the song information from another computer and displays it.


If you want to use this yourself - this code will need lots of modifications, and you will need multiple dependencies (python3, pygame, PIL).

Both ends are meant to run as a systemd service running `main.py`, and `playerctl` is required for the server.
The client is made to specifically render directly on the `/dev/fb1` framebuffer.

The information is transferred over a TCP socket - so the devices must be on the same network.

In the future I may update this to have better versatility, but that currently does not matter to me as I am just using this for my own desktop music display.


This readme file is primarily to explain this project and its capabilities (and downsides), however it also mentions some changes that would need to be made if you would like to try this.

## Code status

This code is generally suboptimal in many ways, and I am aware of this - however since this is only for my personal use, it's fine.
I am also still not great at programming, but I'm always looking to improve!

If you test this and want to suggest any improvements feel free to open a pull request.

## Features

### Server:

The server hosts a TCP socket on port 7463, where it transmits data to a singular client. Subsequent clients will be unable to connect to the server. 

The server end uses `playerctl` to periodically get information (metadata, position, and if the song is paused) about the currently played song. 
This data then is formatted and sent over a TCP socket. This loop completes every 0.4 seconds to continually update the available information for the client.
Each loop completes 3 `playerctl` calls: metadata, status, and position. These calls all check the players: `subtui`, and `spotify`. You can change this in the code if you would like to use this and want support for other players. 

### Client:

The Client end of Simple Song Display is meant to be run on a Raspberry Pi or similar device with a small display. 
The client first attempts to connect to a server on the set local IP, which by default is the local IP of my personal computer. This can be changed within `main.py` of the client code.

If there is no server with the given IP available when the client starts, it will being a loop checking if the server is now running every 30 seconds until it connects. 

Once connected to the server the client begins the main update loop where it retrieves the song data, and uses `pygame` to create a window and display song information. This display is customizable via the `config.py` file in the client code. This display can be stopped by creating a blank file named `stop_display` in the home directory. By default, this is only checking my specific home directory (`/home/hero`) - This will need to be changed within the code if you want to use this.

![image](/images/physical_display.jpg)

**This display is configured to render directly on to the `/dev/fb1` framebuffer.** I personally use the CUQI 3.5" Raspberry Pi screen from amazon. My screen uses the LCD-Show driver, however I don't think this driver should affect the rendering of Simple Song Display.

If no song is currently playing, a no media screen is rendered instead of the music display. 

### Logging

Simple Song Display features a simple logging system. All major client events or errors that occur will be printed to console, and logged to the `log_file` specified in `config.py`. This can be disabled in `config.py` as well. The server only has basic logging which is printed and not written to a file. 

### Config file
The client end for Simple Song Display features a configuration file called `config.py`. This file is part of the program and cannot be stored in another directory. 

`config.py` features variables to control fonts,font sizes, padding values, heights of different elements, colors, as well as other values. The default config was made to look at normal and good as I could make it, but you can probably make it better (or worse). The config file also has several values which are unused - from either features that I removed, or things that are yet to be implimented. 

## Bugs/issues

- If the server is disconnected while the client is running, the client will freeze and not recover.
- Not all data transfers happen at the exact same time, so the position/time indicator may update slightly inconsistently.
- The server can only handle a single client at a time - in the future it should be adapted to handle multiple... especially for testing while still connected on the external display.
- The program may have major issues or crash if an image in the config does not load (or is missing any variables).

**If for some reason you use this program, and find more bugs that are not listed, please create a GitHub issue and I will do by best to fix it (as long as it is a universal issue and not a result of your setup).**
If you find a fix for something or have an improvement, please create a pull request. 

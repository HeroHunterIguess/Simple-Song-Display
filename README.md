# Simple Song Display
100% human code, no LLMs.

![image](/images/showcase_image.png) ![logo](/images/Simple_Song_Display_icon.png)


Simple Song Display is a song display for a Raspberry Pi (or any* Linux machine) which receives the song information from another computer and displays it.

The information is transferred over a TCP socket - so the devices must be on the same network.

## Code status

This code may be suboptimal in several ways, and I am aware of this - however since this is primarily for my personal use, it's fine.
I am also still not great at programming, but I'm always looking to improve!

If you test this and want to suggest any improvements feel free to open a pull request or issue.

## Features

### Installers:

There are two installer scripts: `client_install.sh` and `server_install.sh`. The server installer should be run on the computer on which you want it to check what you're listening to, it will send that information to the client to display it. These installers are made to use `pacman` to install dependencies. If you are on a distro that does not have pacman, you can still use the installers as long as you have `git` installed and you manually download the rest of the dependencies.

The server requires: `python`, and `playerctl`

The client requires: `python`, and the following python libraries: `pygame`, `pillow`, and `requests`.

The client installer will require the username of the computer that runs the server script, so that it can connect. 

### Server:

The server hosts a TCP socket on port 7463, where it transmits data to a singular client. Subsequent clients will be unable to connect to the server. 

The server end uses `playerctl` to periodically get information (metadata, position, and if the song is paused) about the currently played song. 
This data then is formatted and sent over a TCP socket. This loop completes every 0.4 seconds to continually update the available information for the client.
Each loop completes 3 `playerctl` calls: metadata, status, and position. These calls all check the designated player sources set in `reference.py` when installing the program.

### Client:

The Client end of Simple Song Display is meant to be run on a Raspberry Pi or similar device with a small display. 
The client first attempts to connect to a server with the set host name.

If there is no server with the given IP available when the client starts, it will being a loop checking if the server is now running every 30 seconds until it connects. 

Once connected to the server the client begins the main update loop where it retrieves the song data, and uses `pygame` to create a window and display song information. This display is customizable via the `config.py` file in the client code. This display can be stopped by creating a blank file named `stop_display` in the home directory (if the display is in DirectDraw mode). 

![image](/images/physical_display.jpg)
My usage of Simple Song Display on my desk ^^

**This display is configured to either render directly on to the `/dev/fb1` framebuffer or to create a window based on `display_mode` in `config.py`.** I personally use the CUQI 3.5" Raspberry Pi screen from Amazon with the program directly drawing onto the framebuffer. My screen uses the LCD-Show driver, however I don't think this driver should affect the rendering of Simple Song Display when rendering directly onto the framebuffer.

If no song is currently playing, a clock (or no media screen) is rendered instead of the music display. You can enable/disable the clock in `config.py`.

### Logging

The Simple Song Display client features a simple logging system (although it is disabled by default because you would need to set the default `log_file` path). All major client events or errors that occur will be printed to console, and logged to the `log_file` specified in `config.py`. Logging can be enabled in `config.py`. The server only has basic logging which is printed and not written to a file. 

### Config file
The client end for Simple Song Display features a configuration file called `config.py`. This file is part of the program and cannot be stored in another directory. 

`config.py` features variables to control fonts, font sizes, padding values, heights of different elements, colors, as well as other values. The default config was made to look as normal and good as I could make it, but you can probably make it better (or worse). The config file also has several values which are unused - from either features that I removed, or things that are yet to be implimented. If you remove any variables from the config file it will cause errors and the program will not run. 

## Bugs/issues

- If the server is disconnected while the client is running, the client will freeze and not recover.
- Not all data transfers happen at the exact same time, so the position/time indicator may update slightly inconsistently.
- The server can only handle a single client at a time - in the future it should be adapted to handle multiple... especially for testing while still connected on the external display.
- The program may have major issues or crash if an image in the config does not load (or is missing any variables).

**If you use this program, and find more bugs that are not listed, please create a GitHub issue and I will do by best to fix it (as long as it is a universal issue and not a result of your setup).**
If you find a fix for something or have an improvement, please create a pull request. 

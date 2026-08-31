# Simple Song Display

![image](/images/showcase.png)

## ⚠️ WARNING: THIS IS JUST MADE FOR MY PERSONAL USE

A song display for Raspberry Pi (or any Linux machine) which receives the song information from another computer and displays it.


If you want to use this yourself - this code will need lots of modifications, and you will need multiple dependencies.

The server end is meant to be ran as a systemd service running main.py, playerctl is required for the server.
The Raspberry Pi client is made to specifically render directly on /dev/fb1 via the framebuffer.

The information is transferred over a TCP socket - so the devices must be on the same network.

In the future I may update this to have better versatility, but that currently does not matter to me as I am just using this for my own desktop music display.

## Code status

This code is generally suboptimal in many ways, and I am aware of this - however since this is only for my personal use it's fine.
If you test this and want to suggest any improvements feel free to open a pull request.

## Features

### Server:

The server is hosted on a TCP socket on port 7463, where it transmits data to a singular client.

The server end uses `playerctl` to periodically get information (metadata, position, and if the song is paused) about the currently played song. 
This data then is formatted and sent over a TCP socket. This loop completes every 0.4 seconds to continually update the available information for the client.
Each loop completes 3 `playerctl` calls: metadata, status, and position. These calls all check the players: `subtui`, and `spotify`. You can change this in the code if you would like to use this.

### Client:

The Client end of Simple Song Display is meant to be run on a Raspberry Pi or similar device with a small display. 
The client first attempts to connect to a server on the set local IP, which by default is the local IP of my personal computer. This can be changed within `main.py` of the client code.

Once connected to the server the client begins the main update loop where it retrieves the song data, and uses `pygame` to create a window and display song information. This display is fully customizable via the `config.py` file in the client code. 

![image](/images/physical_display.jpg)

**This display is configured to render directly onto the /dev/fb0 framebuffer of a screen using the LCD-Show driver.** I personally use the CUQI 3.5" Raspberry Pi screen from amazon. 

If no song is currently playing, a no media screen is rendered instead of the music display. 

## Bugs/issues

- If the server is not running at the time the client starts, it will fail to start the client and will instead freeze and never connect to a server that comes online later.
- If the server is disconnected while the client is running, the client will freeze and not recover.
- If the host of the album cover image takes too long to respond, sometimes the album cover will disappear for a single 0.4 second cycle. (This has an intended fix however I am unsure if this bug still exists)
- Not all data transfers happen at the exact same time, so the position/time indicator may update slightly inconsistently.
- The server can only handle a single client at a time - in the future it should be adapted to handle multiple... especially for testing while still connected on the external display.

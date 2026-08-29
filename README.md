# Simple Song Display

![A showcase image of Simple Song Display]((https://github.com/HeroHunterIguess/Simple-Song-Display/blob/main/showcase.png))

## ⚠️ WARNING: THIS IS JUST MADE FOR MY PERSONAL USE

A song display for Raspberry Pi (or any Linux machine) which receives the song information from another computer and displays it.


If you want to use this yourself - this code will need lots of modifications, and you will need multiple dependencies.

The server end is meant to be ran as a systemd service running main.py, playerctl is required for the server.
The Raspberry Pi client is made to specifically render directly on /dev/fb1 via the framebuffer.

In the future I may update this to have better versatility, but that currently does not matter to me as I am just using this for my own desktop music display.

## Code status

This code is generally suboptimal in many ways, and I am aware of this - however since this is only for my personal use it's fine.
If you test this and want to suggest any improvements feel free to open a pull request.

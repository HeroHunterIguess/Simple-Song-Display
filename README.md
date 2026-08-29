# Simple Song Display

## ⚠️ WARNING: THIS IS JUST MADE FOR MY PERSONAL USE

A song display for Raspberry Pi streaming information from another computer

If you want to use this yourself - this code will need lots of modifications, and you will need multiple dependencies.

The server end is meant to be ran as a systemd service running main.py, playerctl is required for the server.
The Raspberry Pi client is made to specifically render directly on /dev/fb1 via the framebuffer.

In the future I may update this to have better versatility, but that currently does not matter to me as I am just using this for my own desktop music display.

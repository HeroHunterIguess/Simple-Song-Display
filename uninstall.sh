#!/bin/bash
### Simple Song Display Uninstaller ###


# Initial info
echo ""
echo ""
echo "############################################"
echo "Simple Song Display uninstaller"
echo "############################################"
echo ""
echo "This will remove the files, and delete the services."
echo "This tries to delete both the client and server, you can run it for either."
echo ""
echo "This will not remove dependencies - as other things might use them."
echo "You can find the dependency list on GitHub in README.md"
echo ""
echo "############################################"
echo ""

read -p "Press enter to uninstall"

# Delete program files
rm -rf simple_song_display

# Remove services files
sudo rm -f /etc/systemd/system/simple-song-server.service
sudo rm -f /etc/systemd/system/simple-song-display.service

echo ""
echo "Finished."

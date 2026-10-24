#!/bin/bash
### Simple Song Server Installer ###

# Show initial information
echo ""
echo ""
echo "###########################################"
echo "Welcome to the Simple Song Server Installer"
echo "###########################################"
echo ""
echo "This will install all dependencies, and setup a systemd service for simple song display."
echo "You will be prompted for the sudo password."
echo ""
echo "###########################################"
echo ""

read -p "Press enter to start the installer"

### Setup ###

# Install/Update dependencies
sudo pacman -S --needed --noconfirm python playerctl git


# Setup installation paths
INSTALL_DIR="$HOME/simple_song_server"
SERVICE_SOURCE="$INSTALL_DIR/Simple-Song-Display/etc/systemd/system/simple-song-server.service"

# Create folder
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"


echo ""
echo "###########################################"
echo "Cloning Simple Song Server code from github"
echo "###########################################"
echo ""


# Clone server code from GitHub
git clone https://github.com/HeroHunterIguess/Simple-Song-Display/
cd Simple-Song-Display

# Remove unecessary files
rm -rf client images .git 
rm -f .gitignore

# Move server folder
cd "$INSTALL_DIR"
mv Simple-Song-Display/server server
cd server


### Configure players ###
echo ""
echo "###########################################"
echo "You can now select up to two sources for Simple Song Display."
echo ""
echo "Simple Song Server will send the song playing on either of these players to the client."
echo ""
echo "If you only want to set one player, then it does not matter what you type in the other source."
echo "###########################################"
echo ""

# Get sources
read -r -p "Enter player source one: " SOURCE_ONE
echo ""
read -r -p "Enter player source two: " SOURCE_TWO

# Write sources to reference file for server
touch reference.py

{ # Write sources to reference file
    echo "### Reference information for Simple Song Server ###"
    echo ""
    echo 'source_one = "'$SOURCE_ONE'"'
    echo 'source_two = "'$SOURCE_TWO'"'
} > reference.py


### Setup service ###
echo ""
echo "###########################################"
echo "Setting up Simple Song Server service"
echo "###########################################"
echo ""

# Update service file
sed -i \
    -e "s|/home/herohunter/Everything/Coding/python projects/Simple Song Display/server/main.py|$INSTALL_DIR/server/main.py|" \
    -e "s|/home/herohunter/Everything/Coding/python projects/Simple Song Display|$INSTALL_DIR/server|" \
    -e "s|User=herohunter|User=$USER|" \
    -e "s|/run/user/1000|/run/user/$(id -u)|g" \
    "$SERVICE_SOURCE"

# Setup service
echo "Moving service to correct directory."
echo ""
sudo mv "$SERVICE_SOURCE" /etc/systemd/system/simple-song-server.service

echo "Enabling service."
echo ""
sudo systemctl daemon-reload
sudo systemctl enable --now simple-song-server.service

echo "Service should be enabled..."

# Remove extra files
echo ""
echo "Cleaning up..."

cd $INSTALL_DIR
rm -rf Simple-Song-Display

echo ""
echo "######################"
echo "Installation complete!"
echo "######################"

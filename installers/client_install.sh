#!/bin/bash
### Simple Song Display client installer ###

# Initial info
echo ""
echo ""
echo "############################################"
echo "Welcome to the Simple Song Display Installer"
echo "############################################"
echo ""
echo "This will install all dependencies, and setup a systemd service for Simple Song Display."
echo "You will be prompted for the sudo password."
echo ""
echo "This installer requires the pacman package manager for dependencies."
echo "The rest of the installer will work without, but for the dependencies you must be on a distro with pacman"
echo ""
echo "############################################"
echo ""

read -p "Press enter to start the installer"

# Install dependencies
sudo pacman -S --needed --noconfirm python python-pygame python-pillow python-requests git


# Setup installation paths
INSTALL_DIR="$HOME/simple_song_display"
SERVICE_SOURCE="$INSTALL_DIR/Simple-Song-Display/etc/systemd/system/simple-song-display.service"

# Create folder
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"


# Get files
echo ""
echo "############################################"
echo "Cloning Simple Song Display code from github"
echo "############################################"
echo ""

# Clone server code from GitHub
git clone https://github.com/HeroHunterIguess/Simple-Song-Display/
cd Simple-Song-Display

# Remove unecessary files
rm -rf server images .git 
rm -f .gitignore

# Move client folder
cd "$INSTALL_DIR"

echo "Setting up folders..."
echo ""

mv Simple-Song-Display/client client
cd client
rm -f archive.txt

touch reference.py

echo ""
echo "############################################"
echo "Please enter the host name of the server"
echo "The server installer would have told you this if you do not know."
echo "############################################"
echo ""

read -r -p "Host name: " HOST

{ # Give server host to client
    echo "### Reference information for Simple Song Display ###"
    echo ""
    echo 'server_hostname = "'$HOST'"'
} > reference.py

echo ""
echo "Created reference file."
echo ""


# Setup systemd service
echo "############################################"
echo "Would you like Simple Song Display to auto start?"
echo ""
echo "This will create a systemd service."
echo "############################################"
echo ""

read -r -p "y/n: " SERVICE
echo ""

if [ $SERVICE == "y" ]; then
    # Update service file
    sed -i \
        -e "s|/home/hero/scripts/simple_song_display|$INSTALL_DIR/client|" \
        -e "s|/home/hero/scripts/simple_song_display/main.py|$INSTALL_DIR/client/main.py|" \
        -e "s|User=hero|User=$USER|" \
        "$SERVICE_SOURCE"
    mv $SERVICE_SOURCE /etc/systemd/system/simple-song-display.service
else
    echo "A systemd service will NOT be created."
    echo ""
    echo "Moving on..."
fi

# Remove extra files
echo ""
echo "Cleaning up..."

cd $INSTALL_DIR
rm -rf Simple-Song-Display

echo ""
echo "######################"
echo "Installation complete!"
echo "######################"
echo ""
echo "You can run Simple-Song-Display via main.py in ~/simple_song_display/client/"
echo ""


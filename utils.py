### Get info of currently playing media ###


import subprocess

last_good_data = None

def get_current_playing():
    global last_good_data

    try:
        # Get position and song metadata
        position = subprocess.run(["playerctl", "--player=subtui,spotify", "position"], capture_output=True, text=True, timeout=1).stdout.strip() 
        metadata = subprocess.run(["playerctl", "--player=subtui,spotify", "metadata", "--format", "{{title}}\t{{artist}}\t{{mpris:artUrl}}\t{{mpris:length}}\t{{album}}"], capture_output=True, text=True, timeout=1).stdout.strip()

        if metadata == "":
            title, artist, artURL, length, album = "", "", "", "", ""
        else:
            title, artist, artURL, length, album = metadata.split("\t")

        # Convert length to seconds
        if length != "":
            length = int(length) / 1000000

        # Save and return good data
        last_good_data = (title, artist, artURL, length, album, position)
        return last_good_data
    # Return last good data if subprocess times out
    except subprocess.TimeoutExpired:
        print("Playerctl timeout, using last known good data")

        if last_good_data is not None:
            return last_good_data
        return "", "", "", "", "", ""

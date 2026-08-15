### Get info of currently playing media ###

import subprocess

last_good_data = None

def get_current_playing():
    global last_good_data

    try:
        #title = subprocess.run(["playerctl", "--player=subtui,spotify", "metadata", "--format", "{{title}}"], capture_output=True, text=True, timeout=1).stdout.strip()
        #artist = subprocess.run(["playerctl", "--player=subtui,spotify", "metadata", "--format", "{{artist}}"], capture_output=True, text=True, timeout=1).stdout.strip()
        #artURL = subprocess.run(["playerctl", "--player=subtui,spotify", "metadata", "--format", "{{mpris:artURL}}"], capture_output=True, text=True, timeout=1).stdout.strip() 
        #length = subprocess.run(["playerctl", "--player=subtui,spotify", "metadata", "--format", "{{mpris:length}}"], capture_output=True, text=True, timeout=1).stdout.strip() 
        #album = subprocess.run(["playerctl", "--player=subtui,spotify", "metadata", "--format", "{{album}}"], capture_output=True, text=True, timeout=1).stdout.strip() 
        position = subprocess.run(["playerctl", "--player=subtui,spotify", "position"], capture_output=True, text=True, timeout=1).stdout.strip() 

        metadata = subprocess.run(["playerctl", "--player=subtui,spotify", "metadata", "--format", "{{title}}\t{{artist}}\t{{mpris:artUrl}}\t{{mpris:length}}\t{{album}}"], capture_output=True, text=True, timeout=1).stdout.strip()

        if metadata == "":
            title, artist, artURL, length, album = "", "", "", "", ""
        else:
            title, artist, artURL, length, album = metadata.split("\t")

        if length != "":
            length = int(length) / 1000000

        last_good_data = (title, artist, artURL, length, album, position)
        return last_good_data
    except subprocess.TimeoutExpired:
        print("playerctl timeout, using last known good data")

        if last_good_data is not None:
            return last_good_data
        return "", "", "", "", "", ""

### Get info of currently playing media ###

import subprocess

def get_current_playing():
    title = subprocess.run("playerctl --player=subtui,spotify metadata --format '{{title}}'", shell=True, capture_output=True, text=True).stdout.strip()
    artist = subprocess.run("playerctl --player=subtui,spotify metadata --format '{{artist}}'", shell=True, capture_output=True, text=True).stdout.strip()
    artURL = subprocess.run("playerctl --player=subtui,spotify metadata --format '{{mpris:artUrl}}'", shell=True, capture_output=True, text=True).stdout.strip() 
    length = subprocess.run("playerctl --player=subtui,spotify metadata --format '{{mpris:length}}'", shell=True, capture_output=True, text=True).stdout.strip() 
    if length != "":
        length = int(length) / 1000000
    album = subprocess.run("playerctl --player=subtui,spotify metadata --format '{{album}}'", shell=True, capture_output=True, text=True).stdout.strip() 
    position = subprocess.run("playerctl --player=subtui,spotify position", shell=True, capture_output=True, text=True).stdout.strip() 

    return title, artist, artURL, length, album, position

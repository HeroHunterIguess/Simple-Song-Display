### UTIL FUNCTIONS ###

import io

def parse_info(data):
    title = ""
    artist = ""
    artURL = ""
    length = ""
    is_playing = ""
    album = ""

    # Split data into individual values
    buffer = io.StringIO(data)
    title = buffer.readline().strip()
    artist = buffer.readline().strip()
    artURL = buffer.readline().strip()
    length = buffer.readline().strip()
    is_playing = buffer.readline().strip()
    album = buffer.readline().strip()
    
    return title, artist, artURL, length, is_playing, album

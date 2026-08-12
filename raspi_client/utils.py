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

def format_time(seconds):
    try:
        seconds = int(float(seconds))
    except ValueError as err:
        print("Error converting properly:", err)
        seconds = int(seconds)

    minutes = seconds // 60;
    remaining_seconds = seconds % 60;

    return f"{minutes}:{remaining_seconds:02d}";

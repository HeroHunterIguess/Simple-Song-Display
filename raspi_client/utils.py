### UTIL FUNCTIONS ###

import io

def parse_info(data):
    title = ""
    artist = ""
    artURL = ""
    length = ""
    is_playing = ""
    album = ""

    if data == "":
        return "null", "null", "https://null.com", 0, False, "null", 0

    # Split data into individual values
    buffer = io.StringIO(data)
    title = buffer.readline().strip()
    artist = buffer.readline().strip()
    artURL = buffer.readline().strip()
    length = buffer.readline().strip()
    is_playing = buffer.readline().strip()
    album = buffer.readline().strip()
    position = buffer.readline().strip()
    
    return title, artist, artURL, length, is_playing, album, position

def format_time(seconds):
    if seconds == "":
        return

    try:
        seconds = int(float(seconds))
    except ValueError as err:
        print("Error converting properly:", err)
        seconds = int(seconds)

    minutes = seconds // 60;
    remaining_seconds = seconds % 60;

    return f"{minutes}:{remaining_seconds:02d}";

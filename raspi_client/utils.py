### UTIL FUNCTIONS ###

import io, song_data

def parse_info(data):
    current_song = song_data.song(
        title = "",
        artist = "",
        album = "",
        album_cover_image = "",
        position = "",
        length = "",
        is_playing = False
    )

    if data == "":
        return "null", "null", "https://null.com", 0, False, "null", 0

    # Split data into individual values
    buffer = io.StringIO(data)
    current_song.title = buffer.readline().strip()
    current_song.artist = buffer.readline().strip()
    current_song.album_cover_image = buffer.readline().strip()
    current_song.length = buffer.readline().strip()
    current_song.is_playing = buffer.readline().strip()
    current_song.album = buffer.readline().strip()
    current_song.position = buffer.readline().strip()
    
    return current_song

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

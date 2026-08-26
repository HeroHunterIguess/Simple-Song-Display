### Util functions ###


import io, song_data, subprocess, config as c

# Parse song metadata into song object
def parse_info(data):
    # Initialize song
    current_song = song_data.song(
        title = "",
        artist = "",
        album = "",
        album_cover_image = "",
        position = "",
        length = "",
        is_playing = False
    )

    # If it isnt real then make it empty
    if data == "":
        current_song.title = ""
        current_song.artist = ""
        current_song.album_cover_image = ""
        current_song.length = ""
        current_song.is_playing = ""
        current_song.album = ""
        current_song.position = ""
    else:
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

# Format time in seconds into minutes:seconds
def format_time(seconds):
    if seconds == "":
        return

    try:
        seconds = int(float(seconds))
    except ValueError as err:
        log_output("Error converting properly: " + str(err))
        seconds = int(seconds)

    minutes = seconds // 60;
    remaining_seconds = seconds % 60;

    return f"{minutes}:{remaining_seconds:02d}";

# Try multiple ways to hide blinking cursor in console
def stop_cursor_blink(raspi):
    if raspi:
        try:
            subprocess.run(["sudo", "tee", "/sys/class/graphics/fbcon/cursor_blink"], input="0".encode(), check=True, text=True)
        except OSError as err:
            log_output("Failed to disable blinking: " + str(err))
    #if raspi:
    #    try:
    #        with open("/sys/class/graphics/fbcon/cursor_blink", "w") as f:
    #            f.write("0")
    #    except OSError as err:
    #        log_output("Failed to disable blinking: " + str(err))

# Add message to log file
def log_output(message):
    if c.output:
        with open(c.log_file, "a") as f:
            f.write(message+"\n")
            print(message)

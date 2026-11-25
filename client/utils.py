### Util functions ###


import io, song_data, subprocess, config as c

# Parse song metadata into song object
def parse_info(data):
    # Initialize song
    song = song_data.song()

    # If it isnt real then make it empty
    if data == "":
        log_output("Data is null - using blank data")
        song.title = "null_data"
        song.artist = "null_data"
        song.album_cover_image = "null_data"
        song.length = "null_data"
        song.is_playing = False
        song.album = "null_data"
        song.position = "null_data"
    else:
        # If song is real
        # Split data into individual values
        buffer = io.StringIO(data)
        song.title = buffer.readline().strip()
        song.artist = buffer.readline().strip()
        song.album_cover_image = buffer.readline().strip()
        song.length = buffer.readline().strip()
        song.is_playing = buffer.readline().strip()
        song.album = buffer.readline().strip()
        song.position = buffer.readline().strip()
        
    return song

# Format time in seconds into minutes:seconds
def format_time(seconds):
    if seconds == "":
        return

    try:
        seconds = int(float(seconds))
    except ValueError as err:
        log_output("Error converting time units properly: " + str(err))
        seconds = int(seconds)

    # Convert/format
    minutes = seconds // 60;
    remaining_seconds = seconds % 60;

    return f"{minutes}:{remaining_seconds:02d}";

# Try to hide blinking cursor in console
def stop_cursor_blink(raspi):
    if raspi:
        try:
            subprocess.run(["sudo", "tee", "/sys/class/graphics/fbcon/cursor_blink"], input="0", check=True, text=True)
        except OSError as err:
            log_output("Failed to disable blinking: " + str(err))

# Add message to log file
def log_output(message):
    if c.output:
        with open(c.log_file, "a") as f:
            f.write(message+"\n")
            print(message)

# Truncate song information
def truncate_text(song):
    if len(song.title) > c.title_truncation_length:
        song.title = song.title[0:c.title_truncation_length] + ".."
    
    if len(song.artist) > c.info_truncation_length:
        song.artist = song.artist[0:c.info_truncation_length] + ".."
    if len(song.album) > c.info_truncation_length:
        song.album = song.album[0:c.info_truncation_length] + ".."

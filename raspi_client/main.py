### Simple Song Display ###
# Display client
# This client runs from a systemctl service on the raspi


# Check if user is main pc or raspberry pi
import os, subprocess, utils, config as c
if "herohunter" not in str(subprocess.run("whoami", shell=True, capture_output=True, text=True)).strip():
    if c.output:
        utils.log_output("Running on raspberry pi.")
    raspi = True
else:
    raspi = False

# Setup and initialization
import pygame, time, socket, requests, io, rendering, song_data, datetime

pygame.display.init()
pygame.font.init()

# Initialize screen
if raspi:
    screen = pygame.Surface(c.display_size)
else:
    screen = pygame.display.set_mode(c.display_size)

# Hide mouse cursor
pygame.mouse.set_visible(False)

# Initialize current song
current_song = song_data.song(
    title = "",
    artist = "",
    album = "",
    album_cover_image = "",
    position = "",
    length = "",
    is_playing = False
)

# Remove external stop condition file
if os.path.exists("/home/hero/stop_display"):
    os.remove("/home/hero/stop_display")

def main():
    # Establish server connection
    host = "192.168.1.126"
    port = 7463

    utils.stop_cursor_blink(raspi)

    # Reset log file
    with open(c.log_file, "w") as f:
        f.write(str(datetime.datetime.now()))

    while True:
        # Try to connect to host
        try: 
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(2.0)

            client_socket.connect((host, port))

            if c.output:
                print("Connected to server", host, "at", port)
            break

        except OSError as err:
            if c.output:
                utils.log_output("Server not found. " + str(err))
            sleep(5)

    try:

        # Begin main loop
        running = True
        while running:
            try:
                data = client_socket.recv(1024).decode("utf-8")
            except socket.timeout:
                continue
            
            if c.output_transfer_info:
                utils.log_output("recieved data:\n" + str(data) + "\n")

            # Get metadata about current song
            current_song = utils.parse_info(data)

            # External shutdown condition
            if raspi:
                if os.path.exists("/home/hero/stop_display"):
                    running = False

            # Make window closeable w/ space on pc
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
            
            # Close instantly instead of finishing loop
            if running == False:
                break

            # Draw on screen
            screen.fill(c.background_color)

            if current_song.title == "null" or current_song.album_cover_image == "" or current_song.title == "":
                rendering.no_media(screen)
            elif c.mode == "Standard":
                # General song information
                rendering.render_standard(screen, current_song)
            elif c.mode == "Centered":
                rendering.render_centered(screen, current_song)
            else:
                if c.output:
                    utils.log_output("No valid mode selected.")
                running = False
                break

            time.sleep(0.4)

            # Convert rendered surface to framebuffer and draw
            if raspi:
                rendering.convert_screen_format_and_draw(screen)
            else:
                pygame.display.flip()

            # Try to stop cursor blink
            utils.stop_cursor_blink(raspi)

    # Close client
    except KeyboardInterrupt:
        if c.output:
            utils.log_output("Client closing")
    
    client_socket.close()

main()
pygame.quit()

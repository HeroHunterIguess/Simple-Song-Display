### Simple Song Display ###
# Display client
# This client runs from a systemctl service on the raspi


# Check if user is main pc or raspberry pi
import os, subprocess, utils, config as c
if "herohunter" not in str(subprocess.run("whoami", shell=True, capture_output=True, text=True)).strip():
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
    utils.log_output("Initialized raspi screen surface.")
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

    utils.log_output("Attempting to stop cursor blink... may fail:")
    utils.stop_cursor_blink(raspi)
    

    # Reset log file
    with open(c.log_file, "w") as f:
        utils.log_output("Initalizing/resetting log file.")
        f.write(str(datetime.datetime.now())+"\n\n")

    # Try to connect to host until it goes through
    while True:
        utils.log_output("Attemping to connect to " + host)
        try: 
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(2.0)

            client_socket.connect((host, port))

            utils.log_output("Connected to server: " + host + " at " + str(port))
            break

        # Retry connection if it fails
        except OSError as err:
            utils.log_output("Server not found. " + str(err))
            sleep(30)

    try:

        # Begin main loop
        running = True
        utils.log_output("Beginning update loop...")

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
                    utils.log_output("Shutting down.")
                    running = False

            # Make window closeable w/ space on pc
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        utils.log_output("Shutting down.")
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
                utils.log_output("No valid mode selected.")
                running = False
                break

            time.sleep(0.4)

            # Convert rendered surface to framebuffer and draw
            if raspi:
                rendering.convert_screen_format_and_draw(screen)
            else:
                pygame.display.flip()

    # Close client
    except KeyboardInterrupt:
        utils.log_output("Client closing from keyboard interrupt.")
    
    client_socket.close()

main()
pygame.quit()

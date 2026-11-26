### Simple Song Display ###
# Display client


# Initial imports
import os, subprocess, utils, reference, config as c

# Get username 
username = str(subprocess.run("whoami", shell=True, capture_output=True, text=True).stdout.strip())

# Setup stuff based on display mode
if c.display_mode == "DirectDraw":
    utils.log_output("Running on raspberry pi.")
    direct = True
else:
    direct = False

# Setup and initialization
import pygame, time, socket, requests, io, rendering, song_data, datetime

pygame.display.init()
pygame.font.init()

# Initialize screen
if direct:
    utils.log_output("Initialized direct screen surface.")
    screen = pygame.Surface(c.display_size)
else:
    screen = pygame.display.set_mode(c.display_size)

# Set window title
pygame.display.set_caption("Simple Song Display")

# Load icon
ssd_icon = pygame.image.load("Simple_Song_Display_icon.png")
pygame.display.set_icon(ssd_icon)

# Initialize current song
current_song = song_data.song()

# Remove external stop condition file
if os.path.exists(f"/home/{username}/stop_display"):
    os.remove(f"/home/{username}/stop_display")


def main():
    # Establish server connection
    host = socket.gethostbyname(reference.server_hostname)

    port = 7463

    # Attempt to stop blinking console cursor
    if direct:
        utils.log_output("Stopping cursor blink...")
        utils.stop_cursor_blink()
    
    # Reset log file
    if c.output:
        with open(c.log_file, "w") as f:
            f.write(str(datetime.datetime.now())+"\n\n")
            f.write("Initalizing/resetting log file.\n")

    # Try to connect to host until it goes through
    while True:
        utils.log_output("Attemping to connect to " + host)
        try: 
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(2.0)

            client_socket.connect((host, port))

            utils.log_output(f"Connected to server: {host} at port {port}")
            break

        # Retry connection if it fails
        except OSError as err:
            utils.log_output(f"Server not found: {err}")
            utils.log_output("Waiting 30 seconds before trying again.")
            time.sleep(30)


    try:
        # Begin main loop
        running = True
        utils.log_output("Beginning update loop...")

        while running:
            try:
                # Recieve data
                data = client_socket.recv(1024).decode("utf-8")
            except socket.timeout:
                continue
            
            if c.output_transfer_info:
                utils.log_output(f"Recieved data:\n{data}\n")

            # Parse metadata about current song
            current_song = utils.parse_info(data)

            # External shutdown condition
            if os.path.exists(f"/home/{username}/stop_display"):
                utils.log_output("Shutting down.")
                running = False

            # Make window closeable w/ space on pc
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        utils.log_output("Shutting down.")
                        running = False
                # Close with quit/x
                if event.type == pygame.QUIT:
                    running = False
            
            # Close instantly instead of finishing loop
            if running == False:
                break

            # Draw on screen
            screen.fill(c.background_color)

            if current_song.title == "null_data" or current_song.album_cover_image == "" or current_song.title == "null_data":
                rendering.no_media(screen)
            else:
                rendering.render(screen, current_song)

            time.sleep(0.4)

            # Convert rendered surface to framebuffer and draw
            if direct:
                rendering.convert_screen_format_and_draw(screen)
            else:
                pygame.display.flip()

    # Close client
    except KeyboardInterrupt:
        utils.log_output("Client closing from keyboard interrupt.")
    
    client_socket.close()


main()
pygame.quit()

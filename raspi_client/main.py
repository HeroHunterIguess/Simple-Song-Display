# Simple Song Display

# Setup correct video driver for when there is no DE installed
import os, subprocess
if "herohunter" not in str(subprocess.run("whoami", shell=True, capture_output=True, text=True)).strip():
    if c.output:
        print("Switching to KMSDRM.")
    os.environ["SDL_VIDEODRIVER"] = "kmsdrm"

# Setup and initialization
import pygame, utils, time, socket, requests, io, rendering, song_data, config as c

pygame.display.init()
pygame.font.init()

screen = pygame.display.set_mode(c.display_size)

pygame.mouse.set_visible(False)

current_song = song_data.song(
    title = "",
    artist = "",
    album = "",
    album_cover_image = "",
    position = "",
    length = "",
    is_playing = False
)

def main():
    # Establish server connection
    host = "192.168.1.126"
    port = 7463

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Begin loop
    old_url = ""

    try:
        # Connect to host
        try: 
            client_socket.connect((host, port))
        except ConnectionRefusedError as err:
            print("Server not found.", err)
            return

        running = True
        while running:
            data = client_socket.recv(1024).decode("utf-8")
            if c.output:
                print("recieved data:\n" + str(data))

            current_song = utils.parse_info(data)

            # Make window closeable w/ space
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
                rendering.render_standard(screen, current_song, old_url)
            elif c.mode == "Centered":
                rendering.render_centered(screen, current_song, old_url)

            time.sleep(0.3)
            
            old_url = current_song.album_cover_image

            pygame.display.flip()
    except KeyboardInterrupt:
        if c.output:
            print("client closing")
    
    client_socket.close()

main()
pygame.quit()

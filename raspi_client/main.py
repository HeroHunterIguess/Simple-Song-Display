# Simple Song Display

# Setup correct video driver for when there is no DE installed
import os, subprocess
if "herohunter" not in str(subprocess.run("whoami", shell=True, capture_output=True, text=True)).strip():
    print("Switching to KMSDRM.")
    os.environ["SDL_VIDEODRIVER"] = "kmsdrm"

# Setup and initialization
import pygame, utils, time, socket, requests, io, rendering, config as c

pygame.display.init()
pygame.font.init()

screen = pygame.display.set_mode(c.display_size)

pygame.mouse.set_visible(False)


def main():
    # Establish server connection
    host = "192.168.1.126"
    port = 7463

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Begin loop
    position = 1
    old_title = ""
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
            print("recieved data:\n" + str(data))

            title, artist, artURL, length, is_playing, album = utils.parse_info(data)

            if old_title != title:
                position = 1
            
            if old_url != artURL and artURL != "":
                response = requests.get(artURL)
                album_cover_image = pygame.image.load(io.BytesIO(response.content))
                album_cover_image = pygame.transform.smoothscale(album_cover_image, c.album_cover_size)

            # Make window closeable
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    running = False

            # Draw on screen
            screen.fill(c.background_color)

            if c.mode == "Full":
                # General song information
                rendering.render_full(screen, title, artist, album, album_cover_image, position, length)

            time.sleep(0.5)

            if is_playing == "True":
                position += 0.5
            
            old_title = title
            old_url = artURL

            pygame.display.flip()
    except KeyboardInterrupt:
        print("client closing")
    
    client_socket.close()

main()
pygame.quit()

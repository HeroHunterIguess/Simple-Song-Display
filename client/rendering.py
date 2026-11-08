### Render song display ###


# Imports and initalization
import pygame, utils, requests, io, datetime, config as c 
from PIL import Image, ImageFilter, ImageEnhance
pygame.font.init()

# Setup fonts
main_font = pygame.font.SysFont(c.main_font, c.main_font_size, bold=c.main_font_bold)
secondary_font = pygame.font.SysFont(c.secondary_font, c.secondary_font_size, bold=c.secondary_font_bold)
tertiary_font = pygame.font.SysFont(c.secondary_font, c.tertiary_font_size, bold=c.secondary_font_bold, italic=c.tertiary_italic)

no_media_font = pygame.font.SysFont(c.main_font, c.main_font_size * 2, bold=c.main_font_bold)
clock_font = pygame.font.SysFont(c.main_font, c.clock_font_size, bold=c.main_font_bold)

# Initialize album cover cache
cached_album_cover_surface = None
cached_album_cover_link = None


# Loads image with given url
def load_image(song): 
    global cached_album_cover_surface, cached_album_cover_link

    # Check if its not real
    if song.album_cover_image == "" or song.title == "null":
        utils.log_output("Failed to load album cover: No image to load.")
        return None

    # Try to load same as before 
    if song.album_cover_image == cached_album_cover_link:
        return cached_album_cover_surface
    
    # Try to load new image
    try:
        response = requests.get(song.album_cover_image, timeout=2)
        surface = pygame.image.load(io.BytesIO(response.content))
        surface = pygame.transform.smoothscale(surface, c.album_cover_size)
        cached_album_cover_link = song.album_cover_image
        cached_album_cover_surface = surface
        return surface

    # Old cover
    except requests.exceptions.RequestException as err:
        return cached_album_cover_surface

# Load and cache the blurred background
cached_blurred_background_surface = None

def load_blurred_background(song, response):
    global cached_blurred_background_surface, cached_album_cover_link

    # Check if its not real
    if song.album_cover_image == "" or cached_album_cover_link == "null":
        utils.log_output("Failed to load background: No image to load")
        return None
    
    # Load same as before if its cached 
    if song.album_cover_image == cached_album_cover_link and cached_blurred_background_surface is not None:
        return cached_blurred_background_surface
    
    # Load new album cover image, and format/set it up
    try: 
        background_image = Image.open(io.BytesIO(response.content))
        background_image = background_image.filter(ImageFilter.GaussianBlur(radius=c.gaussian_blur_radius))
        background_image = background_image.convert("RGB")
        background_image = ImageEnhance.Brightness(background_image).enhance(c.background_brightness)
        background = pygame.image.fromstring(background_image.tobytes(), background_image.size, background_image.mode)
        background = pygame.transform.smoothscale(background, c.background_image_size)
        return background
    except requests.exceptions.RequestException as err:
        return cached_blurred_background_surface


# Render centered mode
def render_centered(screen, song):

    # Truncate all text
    utils.truncate_text(song)

    # Format times
    song.position = utils.format_time(song.position)
    song.length = utils.format_time(song.length)

    # Get album cover image
    try:
        response = requests.get(song.album_cover_image, timeout=2)
    except requests.exceptions.RequestException as err:
        utils.log_output("Failed to get background image: " + str(err))
        return

    # Setup, darken, blur, and resize background
    background = load_blurred_background(song, response)

    # Load standard album cover
    album_image_surface = load_image(song)

    # Background
    screen.blit(background, (0, 0))

    # Album cover
    try:
        screen.blit(album_image_surface, (
            c.display_size[0] / 2 - c.album_cover_size[0] / 2, 
            c.album_cover_height
        ))
    except TypeError:
        utils.log_output("Album cover failed to load/render")

    # Song name
    title_surface = main_font.render(song.title, True, c.main_text_color)
    screen.blit(title_surface, (
        c.display_size[0] / 2 - (main_font.size(song.title)[0] / 2), 
        c.spacing_one
    ))

    # Artist name
    artist_surface = secondary_font.render(song.artist, True, c.secondary_text_color)
    screen.blit(artist_surface, (
        c.display_size[0] / 2 - (secondary_font.size(song.artist)[0] / 2), 
        c.spacing_two
    ))

    # Album name
    album_surface = tertiary_font.render(song.album, True, c.tertiary_text_color)
    screen.blit(album_surface, (
        c.display_size[0] / 2 - (tertiary_font.size(song.album)[0] / 2), 
        c.spacing_three
    ))

    # Position in song
    position_surface = secondary_font.render(song.position + " / " + song.length, True, c.secondary_text_color)
    screen.blit(position_surface, (
        c.display_size[0] / 2 - (secondary_font.size(song.position+" / "+song.length)[0] / 2), 
        c.spacing_four
    ))

    # Render paused menu
    if song.is_playing == "False":
        overlay_surface = pygame.Surface(c.display_size)
        overlay_surface.set_alpha(c.paused_darkening)
        overlay_surface.fill((0,0,0))
        screen.blit(overlay_surface, (0,0))

        # Try to get and display pause icon
        try:
            response = requests.get(c.pause_icon, timeout=2)

            pause_surface = pygame.image.load(io.BytesIO(response.content))
            pause_surface = pygame.transform.smoothscale(pause_surface, c.album_cover_size)

            screen.blit(pause_surface, (
                c.display_size[0] / 2 - c.album_cover_size[0] / 2, 
                c.album_cover_height
            ))

        except (requests.exceptions.RequestException, pygame.error) as err:
            utils.log_output("Failed to get or load pause icon: " + str(err))

cached_no_media_background = None

# No media screen if no media is playing
def no_media(screen):
    global cached_no_media_background

    # Load background if there is one
    if c.no_media_background_image_link != "" and c.no_media_background_image:
        if cached_no_media_background is None:
            try:
                response = requests.get(c.no_media_background_image_link, timeout=2)
                background_image = pygame.image.load(io.BytesIO(response.content))
                background_image = pygame.transform.smoothscale(background_image, c.display_size)

                cached_no_media_background = background_image
            except requests.exceptions.RequestException as err:
                utils.log_output("Failed to get no media background: " + str(err))
                screen.fill(c.background_color) 
                return

            # Draw background image
            screen.blit(background_image, (0, 0))
        else:
            screen.blit(cached_no_media_background, (0, 0))
    else:
        screen.fill(c.background_color)
    
    # Darken background image
    overlay_surface = pygame.Surface(c.display_size)
    overlay_surface.set_alpha(c.paused_darkening)
    overlay_surface.fill((0,0,0))
    screen.blit(overlay_surface, (0,0))

    # Draw text (clock or no media message)
    if c.no_media_clock:
        
        # Get current time
        current_time = datetime.datetime.now().strftime("%I:%M")
        clock_surface = clock_font.render(current_time, True, c.main_text_color)

        # Render on screen
        screen.blit(clock_surface, (
            (c.display_size[0] / 2) - clock_font.size(current_time)[0] / 2, 
            (c.display_size[1] / 2) - (c.clock_font_size / 2)) 
        )
    else:
        info_surface = no_media_font.render(c.no_media_message, True, c.main_text_color)

        # Render on screen
        screen.blit(info_surface, (
            (c.display_size[0] / 2) - no_media_font.size(c.no_media_message)[0] / 2, 
            (c.display_size[1] / 2) - (c.main_font_size * 2) / 2)
        )

# Convert pygame surface into framebuffer
def convert_screen_format_and_draw(screen):
    with open("/dev/fb1", "wb") as fb:
        fb.write(screen.convert(16, 0).get_buffer())

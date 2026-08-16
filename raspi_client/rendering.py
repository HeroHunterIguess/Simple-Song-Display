### Render song display ###


# Imports and initalization
import pygame, utils, requests, io, config as c 
from PIL import Image, ImageFilter, ImageEnhance
pygame.font.init()

# Setup fonts
main_font = pygame.font.SysFont(c.main_font, c.main_font_size, bold=c.main_font_bold)
secondary_font = pygame.font.SysFont(c.secondary_font, c.secondary_font_size, bold=c.secondary_font_bold)
tertiary_font = pygame.font.SysFont(c.secondary_font, c.tertiary_font_size, bold=c.secondary_font_bold, italic=c.tertiary_italic)

no_media_font = pygame.font.SysFont(c.main_font, c.main_font_size * 2, bold=c.main_font_bold)

# Initialize album cover cache
cached_album_cover_surface = None
cached_album_cover_link = None

# Loads image with given url
def load_image(c_s): 
    global cached_album_cover_surface, cached_album_cover_link

    # Check if its not real
    if c_s.album_cover_image == "" or c_s.title == "null":
        return None

    # Try to load same as before 
    if c_s.album_cover_image == cached_album_cover_link:
        return cached_album_cover_surface
    
    # Try to load new image
    try:
        response = requests.get(c_s.album_cover_image, timeout=2)
        surface = pygame.image.load(io.BytesIO(response.content))
        surface = pygame.transform.smoothscale(surface, c.album_cover_size)
        cached_album_cover_link = c_s.album_cover_image
        cached_album_cover_surface = surface
        return surface

    # Old cover
    except requests.exceptions.RequestException as err:
        return cached_album_cover_surface

# Render standard top left cornermode
def render_standard(screen, c_s): # c_s is current_song

    # Format times
    c_s.position = utils.format_time(c_s.position)
    c_s.length = utils.format_time(c_s.length)

    # Load album cover
    album_image_surface = load_image(c_s)

    # Song name
    title_surface = main_font.render(c_s.title, True, c.main_text_color)
    screen.blit(title_surface, (
        c.album_cover_size[0] + c.horizontal_padding, 
        0)
    )

    # Artist name
    artist_surface = secondary_font.render(c_s.artist, True, c.secondary_text_color)
    screen.blit(artist_surface, (
        c.album_cover_size[0] + c.horizontal_padding, 
        c.main_font_size + c.line_padding
    ))

    # Album name
    album_surface = tertiary_font.render(c_s.album, True, c.tertiary_text_color)
    screen.blit(album_surface, (
        c.album_cover_size[0] + c.horizontal_padding, 
        c.secondary_font_size + c.line_padding) * 2
    )

    # Album cover
    try:
        screen.blit(album_image_surface, (0, 0))
    except TypeError:
        if c.output:
            print("Album cover failed to load and render")

    # Position in song
    position_surface = secondary_font.render(str(c_s.position) + " / " + str(c_s.length), True, c.secondary_text_color)
    screen.blit(position_surface, (
        c.album_cover_size[0] + c.horizontal_padding, 
        c.secondary_font_size + c.line_padding * 3 + (c.line_padding / 2)
    ))

# Render centered mode
def render_centered(screen, c_s): # c_s is current_song

    # Format times
    c_s.position = utils.format_time(c_s.position)
    c_s.length = utils.format_time(c_s.length)

    # Get album cover image
    try:
        response = requests.get(c_s.album_cover_image, timeout=2)
    except requests.exceptions.RequestException as err:
        if c.output:
            print("Failed to get background image:", err)
        return

    # Setup, darken, blur, and resize background
    background_image = Image.open(io.BytesIO(response.content))
    background_image = background_image.filter(ImageFilter.GaussianBlur(radius=c.gaussian_blur_radius))
    background_image = background_image.convert("RGB")
    background_image = ImageEnhance.Brightness(background_image).enhance(c.background_brightness)
    background = pygame.image.fromstring(background_image.tobytes(), background_image.size, background_image.mode)
    background = pygame.transform.smoothscale(background, c.background_image_size)

    # Load standard album cover
    album_image_surface = load_image(c_s)

    # Background
    screen.blit(background, (0, 0))

    # Album cover
    try:
        screen.blit(album_image_surface, (
            c.display_size[0] / 2 - c.album_cover_size[0] / 2, 
            c.album_cover_height
        ))
    except TypeError:
        if c.output:
            print("Album cover failed to load and render")

    # Song name
    title_surface = main_font.render(c_s.title, True, c.main_text_color)
    screen.blit(title_surface, (
        c.display_size[0] / 2 - (main_font.size(c_s.title)[0] / 2), 
        c.spacing_one
    ))

    # Artist name
    artist_surface = secondary_font.render(c_s.artist, True, c.secondary_text_color)
    screen.blit(artist_surface, (
        c.display_size[0] / 2 - (secondary_font.size(c_s.artist)[0] / 2), 
        c.spacing_two
    ))

    # Album name
    album_surface = tertiary_font.render(c_s.album, True, c.tertiary_text_color)
    screen.blit(album_surface, (
        c.display_size[0] / 2 - (tertiary_font.size(c_s.album)[0] / 2), 
        c.spacing_three
    ))

    # Position in song
    position_surface = secondary_font.render(c_s.position + " / " + c_s.length, True, c.secondary_text_color)
    screen.blit(position_surface, (
        c.display_size[0] / 2 - (secondary_font.size(c_s.position+" / "+c_s.length)[0] / 2), 
        c.spacing_four
    ))

    # Render pause icon
    if c_s.is_playing == "False":
        overlay_surface = pygame.Surface(c.display_size)
        overlay_surface.set_alpha(c.paused_darkening)
        overlay_surface.fill((0,0,0))
        screen.blit(overlay_surface, (0,0))

        try:
            response = requests.get(c.pause_icon, timeout=2)

            pause_surface = pygame.image.load(io.BytesIO(response.content))
            pause_surface = pygame.transform.smoothscale(pause_surface, c.album_cover_size)

            screen.blit(pause_surface, (
                c.display_size[0] / 2 - c.album_cover_size[0] / 2, 
                c.album_cover_height
            ))

        except (requests.exceptions.RequestException, pygame.error) as err:
            if c.output:
                print("Failed to get or load pause icon", err)

# Empty screen if no media is playing
def no_media(screen):
    # Load background if there is one
    if c.no_media_background_image_link != "":
        try:
            response = requests.get(c.no_media_background_image_link, timeout=2)
            background_image = pygame.image.load(io.BytesIO(response.content))
            background_image = pygame.transform.smoothscale(background_image, c.display_size)
        except requests.exceptions.RequestException as err:
            if c.output:
                print("Failed to get no-media background", err)
            screen.fill(c.background_color) 
            return

        # Draw background image
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(c.background_color)

    # Draw background and text
    info_surface = no_media_font.render(c.no_media_message, True, c.main_text_color)
    screen.blit(info_surface, (
        (c.display_size[0] / 2) - no_media_font.size(c.no_media_message)[0] / 2, 
        (c.display_size[1] / 2) - (c.main_font_size * 2) / 2)
    )

# Convert pygame surface into framebuffer
def convert_screen_format_and_draw(screen):
    with open("/dev/fb1", "wb") as fb:
        fb.write(screen.convert(16, 0).get_buffer())

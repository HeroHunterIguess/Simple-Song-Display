### Render song display ###

import pygame, utils, requests, io, config as c 
from PIL import Image, ImageFilter, ImageEnhance
pygame.font.init()

main_font = pygame.font.SysFont(c.main_font, c.main_font_size, bold=c.main_font_bold)
secondary_font = pygame.font.SysFont(c.secondary_font, c.secondary_font_size, bold=c.secondary_font_bold)
no_media_font = pygame.font.SysFont(c.main_font, c.main_font_size * 3, bold=c.main_font_bold)

def load_image(old_url, c_s): 
    if old_url != c_s.album_cover_image and c_s.album_cover_image != "" and c_s.title != "null":
        response = requests.get(c_s.album_cover_image)
        c_s.album_cover_image = pygame.image.load(io.BytesIO(response.content))
        c_s.album_cover_image = pygame.transform.smoothscale(c_s.album_cover_image, c.album_cover_size)

# Render standard top left cornermode
def render_standard(screen, c_s, old_url): # c_s is current_song

    c_s.position = utils.format_time(c_s.position)
    c_s.length = utils.format_time(c_s.length)

    load_image(old_url, c_s)

    title_surface = main_font.render(c_s.title, True, c.main_text_color)
    screen.blit(title_surface, (
        c.album_cover_size[0] + c.horizontal_padding, 
        0)
    )

    artist_surface = secondary_font.render(c_s.artist, True, c.secondary_text_color)
    screen.blit(artist_surface, (
        c.album_cover_size[0] + c.horizontal_padding, 
        c.main_font_size + c.line_padding)
    )

    album_surface = secondary_font.render(c_s.album, True, c.secondary_text_color)
    screen.blit(album_surface, (
        c.album_cover_size[0] + c.horizontal_padding, 
        c.secondary_font_size + c.line_padding) * 2
    )

    # Album cover
    screen.blit(c_s.album_cover_image, (0, 0))

    # Position in song
    position_surface = secondary_font.render(str(c_s.position) + " / " + str(c_s.length), True, c.secondary_text_color)
    screen.blit(position_surface, (
        c.album_cover_size[0] + c.horizontal_padding, 
        c.secondary_font_size + c.line_padding) * 3 + (c.line_padding / 2)
    )

# Render centered mode
def render_centered(screen, c_s, old_url): # c_s is current_song

    c_s.position = utils.format_time(c_s.position)
    c_s.length = utils.format_time(c_s.length)

    response = requests.get(c_s.album_cover_image)

    # Setup, darken, and blur background
    background_image = Image.open(io.BytesIO(response.content))
    background_image = background_image.filter(ImageFilter.GaussianBlur(radius=22))
    background_image = background_image.convert("RGB")
    background_image = ImageEnhance.Brightness(background_image).enhance(0.55)
    background = pygame.image.fromstring(background_image.tobytes(), background_image.size, background_image.mode)

    load_image(old_url, c_s)

    # Background
    screen.blit(background, (0, 0))

    # Album cover
    screen.blit(c_s.album_cover_image, (c.display_size[0] / 2 - c.album_cover_size[0] / 2, c.display_size[1] / 2 - c.album_cover_size[1] / 2 - 50))

    title_surface = main_font.render(c_s.title, True, c.main_text_color)
    screen.blit(title_surface, (
        c.display_size[0] / 2 - (main_font.size(" ")[0] * len(c_s.title) / 2), 
        c.display_size[1] / 2 + 40)
    )

    artist_surface = secondary_font.render(c_s.artist, True, c.secondary_text_color)
    screen.blit(artist_surface, (
        c.display_size[0] / 2 - (secondary_font.size(" ")[0] * len(c_s.artist) / 2), 
        c.display_size[1] / 2 + 40 + c.main_font_size + c.line_padding)
    )

# Empty screen if no media is playing
def no_media(screen):
    if c.no_media_background_image_link != "":
        response = requests.get(c.no_media_background_image_link)
        background_image = pygame.image.load(io.BytesIO(response.content))
        background_image = pygame.transform.smoothscale(background_image, c.display_size)

        screen.blit(background_image, (0, 0))
    else:
        screen.fill(c.background_color)

    info_surface = no_media_font.render("No Media.", True, c.main_text_color)
    screen.blit(info_surface, (0, 0))


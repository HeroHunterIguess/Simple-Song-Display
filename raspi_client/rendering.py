### Render song display ###

import pygame, utils, requests, io, config as c 
pygame.font.init()

main_font = pygame.font.SysFont(c.main_font, c.main_font_size, bold=c.main_font_bold)
secondary_font = pygame.font.SysFont(c.secondary_font, c.secondary_font_size, bold=c.secondary_font_bold)
no_media_font = pygame.font.SysFont(c.main_font, c.main_font_size * 3, bold=c.main_font_bold)

def render_standard(screen, c_s): # c_s is current_song

    c_s.position = utils.format_time(c_s.position)
    c_s.length = utils.format_time(c_s.length)

    title_surface = main_font.render(c_s.title, True, c.main_text_color)
    screen.blit(title_surface, (c.album_cover_size[0] + c.horizontal_padding, 0))

    artist_surface = secondary_font.render(c_s.artist, True, c.secondary_text_color)
    screen.blit(artist_surface, (c.album_cover_size[0] + c.horizontal_padding, c.main_font_size + c.line_padding))

    album_surface = secondary_font.render(c_s.album, True, c.secondary_text_color)
    screen.blit(album_surface, (c.album_cover_size[0] + c.horizontal_padding, (c.secondary_font_size + c.line_padding) * 2))

    # Album cover
    screen.blit(c_s.album_cover_image, (0, 0))

    # Position in song
    position_surface = secondary_font.render(str(c_s.position) + " / " + str(c_s.length), True, c.secondary_text_color)
    screen.blit(position_surface, (c.album_cover_size[0] + c.horizontal_padding, (c.secondary_font_size + c.line_padding) * 3 + (c.line_padding)))

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

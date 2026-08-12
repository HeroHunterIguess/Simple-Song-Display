### Render song display ###

import pygame, utils, config as c 
pygame.font.init()

main_font = pygame.font.SysFont(c.main_font, c.main_font_size, bold=c.main_font_bold)
secondary_font = pygame.font.SysFont(c.secondary_font, c.secondary_font_size, bold=c.secondary_font_bold)

def render_full(screen, title, artist, album, album_cover_image, position, length):

    position = utils.format_time(position)
    length = utils.format_time(length)

    title_surface = main_font.render(title, True, c.main_text_color)
    screen.blit(title_surface, (c.album_cover_size[0] + c.horizontal_padding, 0))

    artist_surface = secondary_font.render(artist, True, c.secondary_text_color)
    screen.blit(artist_surface, (c.album_cover_size[0] + c.horizontal_padding, c.main_font_size + c.line_padding))

    album_surface = secondary_font.render(album, True, c.secondary_text_color)
    screen.blit(album_surface, (c.album_cover_size[0] + c.horizontal_padding, (c.secondary_font_size + c.line_padding) * 2))

    # Album cover
    screen.blit(album_cover_image, (0, 0))

    # Position in song
    position_surface = secondary_font.render(str(position) + " / " + str(length), True, c.secondary_text_color)
    screen.blit(position_surface, (0, (c.secondary_font_size + c.line_padding) * 3 + (c.line_padding * 2)))

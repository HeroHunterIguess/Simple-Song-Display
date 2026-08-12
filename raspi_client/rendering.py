### Render song display ###

import config as c 

def render_full(screen, font, title, artist, album, album_cover_image, position, length):
    title_surface = font.render(title, True, c.main_text_color)
    screen.blit(title_surface, (c.album_cover_size[0] + c.horizontal_padding, 0))

    artist_surface = font.render(artist, True, c.secondary_text_color)
    screen.blit(artist_surface, (c.album_cover_size[0] + c.horizontal_padding, c.font_size + c.line_padding))

    album_surface = font.render(album, True, c.secondary_text_color)
    screen.blit(album_surface, (c.album_cover_size[0] + c.horizontal_padding, (c.font_size + c.line_padding) * 2))

    # Album cover
    screen.blit(album_cover_image, (0, 0))

    # Position in song
    position_surface = font.render(str(position) + " / " + str(length), True, c.secondary_text_color)
    screen.blit(position_surface, (0, (c.font_size + c.line_padding) * 3))

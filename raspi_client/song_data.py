### Song info ###

from dataclasses import dataclass

@dataclass
class song:
    title: str
    artist: str
    album: str
    album_cover_image: str
    position: str
    length: str
    is_playing: bool

from items.Gif import Gif
from items.Song import Song


class MoodItem:

    song: Song
    gif: Gif

    def __init__(self, song: Song, gif: Gif):
        self.song = song
        self.gif = gif

    def __repr__(self):
        return f"SONG: {self.song} | GIF: {self.gif}"

    def get_song_mood_vec(self):
        return self.song.energy, self.song.valence

    def get_song_url(self):
        return self.song.href

    def get_song_title(self):
        return self.song.title

    def get_song_artist(self):
        return self.song.artist

    def get_gif_url(self):
        return self.gif.original_url()

    def get_gif_keywords(self):
        return self.gif.keywords


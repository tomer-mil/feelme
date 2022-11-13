from copy import deepcopy
from items.MoodVec import MoodVec


class Song:

    # Class Attributes
    title: str
    artist: str
    mood_vec: MoodVec
    spotify_ID: str
    href: str

    def __init__(self,
                 title: str,
                 artist: str,
                 spotify_ID: str = None,
                 href: str = None,
                 mood_vec: MoodVec = None):

        self.title = title
        self.artist = artist
        self.mood_vec = mood_vec
        self.spotify_ID = spotify_ID
        self.href = href

    def __repr__(self):
        return f"<title: {self.title}, by: {self.artist} | ID: {self.spotify_ID}>"

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def get_title(self):
        return self.title

    def get_artist(self):
        return self.artist

    def get_id(self) -> str:
        return self.spotify_ID

    def get_mood_vec(self):
        return self.mood_vec

    def get_href(self):
        return self.href







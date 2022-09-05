class Song:

    # Class Attributes
    spotify_ID: str
    href: str
    title: str
    artist: str
    energy: int
    valence: int

    def __init__(self,
                 title: str,
                 artist: str,
                 spotify_ID: str = None,
                 href: str = None,
                 energy: int = None,
                 valence: int = None):

        self.spotify_ID = spotify_ID
        self.href = href
        self.title = title
        self.artist = artist
        self.energy = energy
        self.valence = valence

    def __repr__(self):
        return f"<title: {self.title}, by: {self.artist} | ID: {self.spotify_ID}>"

    def get_title(self):
        return self.title

    def get_artist(self):
        return self.artist

    def get_id(self) -> str:
        return self.spotify_ID

    def get_mood_vec(self):
        return self.energy, self.valence

    def get_href(self):
        return self.href







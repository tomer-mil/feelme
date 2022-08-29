class Song:

    # Class Attributes
    spotify_ID: str
    href: str
    title: str
    artist: str
    energy: int
    valence: int

    def __init__(self,
                 spotify_ID: str,
                 href: str,
                 title: str,
                 artist: str,
                 energy: int,
                 valence: int):

        self.spotify_ID = spotify_ID
        self.href = href
        self.title = title
        self.artist = artist
        self.energy = energy
        self.valence = valence

    def __repr__(self):
        return f"<title: {self.title} | by: {self.artist} | ID: {self.spotify_ID}>"






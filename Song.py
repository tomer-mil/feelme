class Song:

    # Class Attributes
    title: str
    artist: str
    spotify_ID: str
    spotify_url: str
    energy: int
    valence: int

    def __init__(self,
                 title: str,
                 artist: str,
                 energy: int=-1,
                 valence: int=-1,
                 spotify_ID: str=""):

        self.title = title
        self.artist = artist
        self.energy = energy
        self.valence = valence
        self.spotify_ID = spotify_ID

    def __repr__(self):
        return f"<title: {self.title} | by: {self.artist} | ID: {self.spotify_ID}>"

    def set_spotify_info(self, url: str, id: str):
        self.spotify_ID = id
        self.spotify_url = url





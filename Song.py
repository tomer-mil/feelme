class Song:
    def __init__(self,
                 title: str,
                 artist: str,
                 sentiments: list=None,
                 energy: int=-1,
                 valence: int=-1,):

        self.title = title
        self.artist = artist
        self.sentiments = sentiments
        self.energy = energy
        self.valence = valence
        self.spotify_ID = ''
        self.giphy_url = ''

    def __repr__(self):
        return f"<{self.title} | {self.artist}>"

    def __setattr__(self, key, value):
        match key:
            case "title":
                # if value is not isinstance(value, str):
                #     raise
                self.title = value
            case "artist":
                self.artist = value
            case "sentiments":
                self.sentiments = value
            case _:
                print("No such attribute to assign to")



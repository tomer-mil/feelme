from Utils import clean_gif_url


class Gif:
    def __init__(self, giphy_id: str,
                 keywords: str,
                 images: dict):
        self.giphy_id = giphy_id
        self.keywords = keywords
        self.images = images  # TODO: getting all "images" dict from giphy API. Need to check what data is relevant.

    def __repr__(self):
        return f"<URL: {self.original_url()} | ID: {self.giphy_id} | Keywords: {self.keywords}>"

    def get_id(self) -> str:
        return self.giphy_id

    def original_url(self) -> str:
        url = self.images["original"]["url"]
        return clean_gif_url(url)

    def original_webp(self) -> str:
        webp = self.images["original"]["webp"]
        return clean_gif_url(webp)

    def downsized_url(self, size: str = ""):
        if size != "":
            size += f"_{size}"
        url = self.images[size]["url"]
        return clean_gif_url(url)



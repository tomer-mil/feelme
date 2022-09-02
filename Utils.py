from urllib.parse import urlparse

########################
# GIF SERVER UTILITIES #
########################

def clean_gif_url(url: str) -> str:
    parsed_url = urlparse(url=url)
    return parsed_url._replace(params="").geturl()


def create_keywords_query(keywords: list) -> str:
    dirty_query = "".join(f"{key}, " for key in keywords)
    return dirty_query[:-2]

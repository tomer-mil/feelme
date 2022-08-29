import json
from urllib import parse, request

from Gif import Gif

#############
# CONSTANTS #
#############

SEARCH_URL = "http://api.giphy.com/v1/gifs/search"
GIF_LIMIT = 3
RESULTS_RATING = "pg"


def get_giphy_url():
    pass


def get_keywords():
    pass


def create_gif(query: str):
    keywords = get_keywords()
    giphy_url = get_giphy_url()
    return Gif(keywords=keywords, url=giphy_url)
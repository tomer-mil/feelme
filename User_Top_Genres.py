import tekore as tk
from Utils import ENV_PATH
from dotenv import load_dotenv
from Authorization import authorize
import os


def get_top_artists():

    # first, authorize as a spotify account
    spotify = authorize()[0]

    # get access token from .env file
    load_dotenv()
    access_token = os.getenv(key='USER_ACCESS_TOKEN')

    with spotify.token_as(access_token):
        top_artists = [artist.name for artist in spotify.current_user_top_artists(time_range='long_term').items[:]]

    return top_artists


print(get_top_artists())
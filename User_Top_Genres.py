import tekore as tk
from Utils import ENV_PATH
from dotenv import load_dotenv
from Authorization import authorize
from itertools import chain
from collections import OrderedDict
import os


###### CONSTANTS ######
ITEMS_LIM = 50  # any number from 1 to 50
TIME_RANGE = 'long_term'  # can also use short_term or medium_term


###### HELPER FUNCS ######
def histogram(lst):
    """
    The histogram function takes a list of integers and returns a dictionary with the number of times each integer
    appears in the list. For example, histogram([4, 9, 7]) should return {4: 1, 9: 1, 7: 1}

    :param lst: Represent the list of values that will be used to create the histogram
    :return: A dictionary with the number of times each item appears in the list
    """
    hist = {}
    for item in lst:
        hist[item] = hist.get(item, 0) + 1
    return hist


# first, authorize as a spotify account
spotify = authorize()[0]

# get access token from .env file
load_dotenv()
access_token = os.getenv(key='USER_ACCESS_TOKEN')


def get_top_artists():
    """
    The get_top_artists function returns a list of the top artists for the user.
    It returns a list of FullArtist tekore objects, which are implemented as dictionaries, containing all artist's info.

    :return: A list of the top artists for a user
    """
    with spotify.token_as(access_token):
        top_artists = [artist for artist in spotify.current_user_top_artists(time_range=TIME_RANGE,
                                                                             limit=ITEMS_LIM).items]
    return top_artists


def get_top_tracks():
    """
    The get_top_tracks function returns a list of the user's top tracks. It returns a list of tekore FullTrack objects.

    :return: A list of dictionaries, each dictionary representing a track
    """
    with spotify.token_as(access_token):
        top_tracks = [track for track in spotify.current_user_top_tracks(time_range=TIME_RANGE,
                                                                         limit=ITEMS_LIM).items]
    return top_tracks


def get_artists_genres() -> list:
    """
    The get_artists_genres function returns a list of genres for the top artists in your library.

    :return: A list of all the genres in the top artists
    """
    top_artists = get_top_artists()
    genres_list = [artist.genres for artist in top_artists]
    genres_list = list(chain(*genres_list))  # "*" unpacks the list in the function, since chain works on iterables
    return genres_list


def hist_genres(lst) -> dict:
    """
    The hist_genres function takes a list of genres and returns a dictionary with the number of times each genre appears
    in the list.
    The function sorts the dictionary by value, from greatest to least, and returns it as a new dictionary.

    :param lst: Pass in a list of genres
    :return: A dictionary of the genres and their frequencies
    """
    hist = histogram(lst)
    sorted_tuples = sorted(hist.items(), key=lambda x: x[1], reverse=True)
    hist = dict(sorted_tuples)
    return hist

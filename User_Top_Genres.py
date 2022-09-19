import tekore as tk
from Utils import ENV_PATH
from dotenv import load_dotenv
from Authorization import get_spotify
from itertools import chain
import os


##############
# CONSTANTS #
##############
ITEMS_LIM = 50  # any number from 1 to 50
TIME_RANGE = 'long_term'  # can also use short_term or medium_term


#################
# HELPER FUNCS #
#################

def histogram(lst: list[int]) -> dict:
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


def get_access_token() -> str:
    """
    The get_access_token function returns the user's access token from the environment variable.
    :return: A tk.Token as a string
    """
    load_dotenv()
    access_token = os.getenv(key='USER_ACCESS_TOKEN')
    return access_token


##################
# AUTHORIZATION #
##################

spotify = get_spotify()
access_token = get_access_token()

###################
# MAIN FUNCTIONS #
###################


def get_top_artists() -> list[tk.model.FullArtist]:
    """
    The get_top_artists function returns a list of the top artists for the user.
    It returns a list of FullArtist tekore objects, which are implemented as dictionaries, containing all artist's info.

    :return: A list of the Full Artists (from the tekore library)
    """
    with spotify.token_as(access_token):
        top_artists = [artist for artist in spotify.current_user_top_artists(time_range=TIME_RANGE,
                                                                             limit=ITEMS_LIM).items]
    return top_artists


def get_top_tracks() -> list[tk.model.FullTrack]:
    """
    The get_top_tracks function returns a list of the user's top tracks. It returns a list of tekore FullTrack objects.

    :return: A list of Full Track (from the tekore library)
    """
    with spotify.token_as(access_token):
        top_tracks = [track for track in spotify.current_user_top_tracks(time_range=TIME_RANGE,
                                                                         limit=ITEMS_LIM).items]
    return top_tracks


def get_users_top_artists_genres() -> list[str]:
    """
    The get_users_top_artists_genres function returns a list of genres for the top artists in user's library.

    :return: A list of all the genres of the user's top artists
    """
    top_artists = get_top_artists()
    genres_list = [artist.genres for artist in top_artists]  # This creates a list of lists, as artist.genres is a
    # list itself.
    genres_list = list(chain(*genres_list))  # This turns genres_list to a 1-D list,
    # "*" unpacks the list in the function, since chain works on iterables
    return genres_list


def hist_genres_helper(lst) -> dict[str]:
    """
    The hist_genres_helper function takes a list of genres and returns a dictionary with the number of times each genre appears
    in the list.
    The function sorts the dictionary by value, from greatest to least, and returns it as a new dictionary.

    :param lst: Pass in a list of genres
    :return: A dictionary of the genres (keys) and their frequencies (values)
    """
    hist = histogram(lst)
    sorted_tuples = sorted(hist.items(), key=lambda x: x[1], reverse=True)
    hist = dict(sorted_tuples)
    return hist


def hist_genres() -> dict[str]:
    """
    The hist_genres function takes in a list of genres, and returns an histogram, implemented as a dictionary
    with the number of times each genre appears.

    :return: A dictionary of the genres (keys) and their frequencies (values)
    """
    genres_list = get_users_top_artists_genres()
    return hist_genres_helper(genres_list)

import json
import dotenv
from urllib import parse, request
from Gif import Gif

#############
# CONSTANTS #
#############

SEARCH_URL = "https://api.giphy.com/v1/gifs/search?"
GIF_LIMIT = 1
RESULTS_RATING = "pg"
RESULTS_LANGUAGE = "en"
GIPHY_API_KEY = dotenv.get_key(dotenv_path=dotenv.find_dotenv(), key_to_get="GIPHY_KEY")

#######################


def set_giphy_search_url(query: str) -> str:
    """
    The set_giphy_search_url function takes a query string and returns the URL for the Giphy API call.

    :param query:str: Input query to search the Giphy API
    :return: The url of the api call that will be used to get a gif
    """
    api_call = {
        "api_key": GIPHY_API_KEY,
        "q": query,
        "limit": GIF_LIMIT,
        "offset": 0,
        "rating": RESULTS_RATING,
        "lang": RESULTS_LANGUAGE
    }
    api_call_url = parse.urlencode(query=api_call, doseq=True)

    return SEARCH_URL + api_call_url


def call_giphy_api(request_url: str):  # TODO: Error handling
    """
    The search_gif function takes a request URL as an argument, calls the Giphy API and returns the results of that search in JSON format.
    The function uses the Giphy API to make a GET request to their public API, which is documented at https://developers.giphy.com/docs/api#quick-start-guide

    :param request_url:str: A formatted URL to call the API with
    :return: A dictionary of gif data retrieved fro Giphy
    """
    with request.urlopen(url=request_url) as response:
        data = json.loads(response.read())
    return data


################
# MAIN METHOD #
################


def search_gif(query: str) -> Gif:
    """
    The create_gif function takes a list of keywords and returns a Gif object.
    The function first creates the query string using the create_keywords_query function, then uses that query to search for gifs on giphy.com.
    It then takes the data from that search and creates a new Gif object with it's giphy id, keywords, and images.

    :param query:list: Pass in a list of keywords to be used
    :return: A gif object
    """
    request_url = set_giphy_search_url(query=query)

    gif_data = call_giphy_api(request_url=request_url).get("data")

    new_gif = Gif(giphy_id=gif_data[0].get("id"),
                  keywords=query,
                  images=gif_data[0].get("images"))

    return new_gif

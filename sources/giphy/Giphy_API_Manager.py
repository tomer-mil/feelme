import json
import dotenv
from urllib import parse, request


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
    :return: A dictionary of gif data retrieved from Giphy
    """
    with request.urlopen(url=request_url) as response:
        data = json.loads(response.read())
    return data


def get_gif_data_from_giphy(keywords_list: list[str]) -> dict:
    keywords_str = " ,".join(keywords_list)
    request_url = set_giphy_search_url(query=keywords_str)
    gif_data = call_giphy_api(request_url=request_url).get("data")

    return gif_data

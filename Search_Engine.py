from MoodItem import MoodItem
import Utils
from OpenAI_API_Manager import get_OpenAI_analysis
from Giphy_API_Manager import search_gif
from Song import Song

#############
# CONSTANTS #
#############


RESPONSE_SEPERATOR = "|"
OPENAI_PROMPT_PREFIX1 = "find a real song that represents the emotions coming from this text:"
OPENAI_PROMPT_PREFIX = "find a real song that reflects the emotions coming from this text:"
OPENAI_PROMPT_SUFFIX = f"song title, artist {RESPONSE_SEPERATOR} list of emotions {RESPONSE_SEPERATOR} 2 keywords from text"


#####################
# ASSISTIVE METHODS #
#####################


def generate_prompt(query: str) -> str:
    """
    The generate_prompt function takes in a string of text entered by the user (his story) and returns a ready-to-use
    query for the OpenAI server to analyze



    :param query:str: Store the user's text (story) that will be used to generate a query
    :return: A string that will be used as a query for the openai server
    """
    prompt = f"{OPENAI_PROMPT_PREFIX} \"{query}\"\n{OPENAI_PROMPT_SUFFIX}"
    return prompt


def parse_OpenAI_response(response) -> dict:
    """
    The parse_OpenAI_response function takes in a response from the OpenAI API and parses it into a dictionary.
    The function first fetches the relevant text from the response, and then splits the text of the response by
    the constant seperator. The function then extracts these values using extract methods and returns them as a dictionary.

    :param response: Pass in the response from the api
    :return: A dictionary with the following keys:
    """

    total_text = response["choices"][0]["text"].split(RESPONSE_SEPERATOR)
    mooditem_dict = {}

    song_info = Utils.extract_song_title_and_artist(total_text[0].strip())  # title and artist
    prompt_sentiments = Utils.extract_sentiments(total_text[1].strip())  # sentiments
    prompt_keywords = Utils.extract_keywords(total_text[2].strip().strip('"'))  # keywords

    mooditem_dict.update(song_info)
    mooditem_dict.update(prompt_sentiments)
    mooditem_dict.update(prompt_keywords)

    """
    mooditem_dict = {
        "title": str,
        "artist": str,
        "sentiments": list[str],
        "keywords": list[str]
    }
    """

    return mooditem_dict


def query_to_data_dict(query: str) -> dict:
    openai_response = get_OpenAI_analysis(prompt=query)
    return parse_OpenAI_response(openai_response)


################
# MAIN METHODS #
################


def search(query: str) -> MoodItem:
    prompt = generate_prompt(query=query)

    data_dict = query_to_data_dict(query=prompt)

    gif = search_gif(keywords=data_dict["keywords"])

    anchor_song = Song(title=data_dict["title"], artist=data_dict["artist"])
    # song = search_song_with_anchor(anchor=anchor_song)  # TODO: Write this func :)

    return MoodItem(song=anchor_song, gif=gif)

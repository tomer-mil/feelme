from MoodItem import MoodItem
from MoodVec import MoodVec
from OpenAI_API_Manager import get_OpenAI_analysis
from Giphy_API_Manager import search_gif
from Text_Analyzer import multiple_texts_analysis
from Song import Song
import Utils

#############
# CONSTANTS #
#############


RESPONSE_SEPERATOR = "|"
OPENAI_PROMPT_PREFIX1 = "find a real song that represents the emotions coming from this text:"
OPENAI_PROMPT_PREFIX = "find a real song that reflects the emotions coming from this text:"
OPENAI_PROMPT_SUFFIX = f"song title, artist {RESPONSE_SEPERATOR} list of emotions {RESPONSE_SEPERATOR} 2 keywords from text"

QUERY_WEIGHT = 0.3
SENTIMENTS_WEIGHT = 0.7


###########################
# OPENAI ANALYSIS METHODS #
###########################


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
        "sentiments": str,
        "keywords": list[str]
    }
    """

    return mooditem_dict


##########################
# SONG SEARCHING METHODS #
##########################

def search_song(text: str, sentiments: str):
    """
    The search_song takes a parsed query i.e a text-sentiments pair, creates their weighted mood vector and searches
    the mood-song db for the song with mood values closest to the weighted mood vector, and returns it.

    :param text: The original text input by the user
    :param sentiments: The parsed sentiments from the text
    :return: Song object with the suggested song from db
    """
    text_mood_vec = calc_query_mood_vec(text=text, sentiments=sentiments)
    # search_song_by_mood(mood_vec=text_mood_vec)
    return text_mood_vec


def weighted_mood_vec(text_info: dict, sentiments_info: dict) -> MoodVec:
    """
    The weighted_mood_vec function takes a dictionary with mood information and analysis rating
    for both text and sentiments. It then calculates the values with a weighted average based on weights
    given upfront in order to generate a weighted mood vector representing the user's initial query.

    :param text_info: The text's data_dict
    :param sentiments_info: The sentiments' data_dict
    :return: MoodVec object representing the query's mood values
    """

    t_mood_vec = MoodVec(energy=text_info["energy"],
                         valence=text_info["valence"])

    s_mood_vec = MoodVec(energy=sentiments_info["energy"],
                         valence=sentiments_info["valence"])

    # TODO: Write an algorithm taking in concern the analysis rating
    # q_rating = query_info["rating"]
    # s_rating = sentiments_info["rating"]

    w_energy = QUERY_WEIGHT * t_mood_vec.energy + SENTIMENTS_WEIGHT * s_mood_vec.energy
    w_valence = QUERY_WEIGHT * t_mood_vec.valence + SENTIMENTS_WEIGHT * s_mood_vec.valence

    return MoodVec(energy=w_energy, valence=w_valence)


def calc_query_mood_vec(text: str, sentiments: str) -> MoodVec:
    """
    the calc_query_mood_vec takes a string text and parsed sentiments and returns a ready-to-use mood vector

    :param text:str: User's text in the query
    :param sentiments:str: Parsed sentiments from the query
    :return: MoodVec object ready-to-use for searching
    """
    analyzed_texts = multiple_texts_analysis(text, sentiments)
    print(f"text analysis:\n{analyzed_texts[0]}\nsenti analysis:\n{analyzed_texts[1]}")
    return weighted_mood_vec(text_info=analyzed_texts[0], sentiments_info=analyzed_texts[1])

###############################
# GENERAL INFORMATION METHODS #
###############################


def query_to_data_dict(query: str) -> dict:
    """
    The query_to_data_dict function takes a query string as input and returns a dictionary with parsed data.
    The returned dictionary contains the following keys:
        - text: The original query string.
        - sentiments: Parsed sentiments from the query, by OpenAI.
        - keywords: Parsed keywords of the text by OpenAI.
        - title: DEPRECATED Anchor song's title.
        - artist: DEPRECATED Anchor song's artist.

    :param query:str: Query to be parsed by OpenAI
    :return: A dictionary with the keys above.
    """
    data_dict = {
        "text": query
    }

    prompt = generate_prompt(query=query)
    openai_response = get_OpenAI_analysis(prompt=prompt)

    data_dict.update(parse_OpenAI_response(openai_response))
    return data_dict


######################
# MAIN SEARCH METHOD #
######################
def search(query: str) -> MoodItem:
    """
    The search function takes a query string and returns a MoodItem object with ready to populate
    song and gif information.

    :param query:str: Pass in the query string from the user
    :return: MoodItem object

    """
    data_dict = query_to_data_dict(query=query)

    gif = search_gif(query=data_dict["keywords"])
    song = search_song(text=data_dict["text"], sentiments=data_dict["sentiments"])
    print(f"gif:\n{gif}\nsong values:\n{song}")
    return MoodItem(song=Song(title="test", artist="test"), gif=gif)


search("The wolf continued down the lane and he passed by the second house made of sticks; and he saw the house, and he smelled the pigs inside, and his mouth began to water as he thought about the fine dinner they would make.")
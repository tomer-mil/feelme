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


####################################
# OPENAI SERVER RESPONSE UTILITIES #
####################################


def extract_song_title_and_artist(response_text: str) -> dict:
    """
    The extract_song_title_and_artist function takes a string as an argument and returns a dictionary containing the song title
    and artist. The function splits the string and then strips whitespace from both ends of each substring before
    returning the dictionary.

    :param response_text:str: Pass in the text from the response object
    :return: A dictionary with the song title and artist
    """

    response_text_list = response_text.split("by")

    for i, info in enumerate(response_text_list):
        response_text_list[i] = info.strip().strip('"')

    song_info = {
        "title": response_text_list[0],
        "artist": response_text_list[1]
    }

    return song_info


def extract_sentiments(response_sentiments_text: str) -> dict:
    """
    The extract_sentiments function takes a string of comma-separated sentiments and returns a dictionary with the
    sentiments. The extract_sentiments function assumes that each sentiment in
    the input string is separated by a comma followed by a space. If there are multiple commas in the text or if
    there are no commas at all, then an empty dictionary will be returned.

    :param response_sentiments_text:str: Store the sentiments from the response of the api call
    :return: A dictionary with a list of strings as the value for the key "sentiments";
    """
    prompt_sentiments = {
        "sentiments": response_sentiments_text.split(', ')
    }
    return prompt_sentiments


def extract_keywords(response_keywords_text: str) -> dict:
    """
    The extract_keywords function takes a string of keywords from the API response and returns a dictionary
    containing the list of keywords. The function strips any leading or trailing whitespace, removes any commas,
    and removes double quotes.

    :param response_keywords_text:str: Pass the text that is returned from the OpenAI api call
    :return: A dictionary with a single key:value pair, where the value is a list of keywords
    """
    keywords_list = response_keywords_text.split(" ")
    for i, keyword in enumerate(keywords_list):  # reminder: .strip() method is NOT in-place
        keywords_list[i] = keyword.strip(',').strip('"')
    prompt_keywords = {
        "keywords": keywords_list
    }
    return prompt_keywords


############################
# QUERY ANALYSIS UTILITIES #
############################

def clean_word(word: str) -> str:
    if not word.isalpha():
        word = word.replace(",", "").replace("-", " ")
        word = word.strip("(").strip(")").strip("!")
    return word.lower()

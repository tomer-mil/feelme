import os
import json
from dotenv import load_dotenv
import openai
from OpenAIConfig import config

# CONSTANTS
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
EXAMPLE_PATH = "/Users/tomermildworth/Desktop/Coding/FeelMe/feelme"
EXAMPLE_QUERY = "I just failed my last test and i dont know how things are going to turn out. im bumped and have zero energy"
RESPONSE_SEPERATOR = "|"

###############


def generate_prompt(text: str):
    """
    The generate_prompt function takes in a string of text entered by the user (his story) and returns a ready-to-use
    query for the OpenAI server to analyze



    :param text:str: Store the user's text (story) that will be used to generate a query
    :return: A string that will be used as a query for the openai server
    :doc-author: Trelent
    """
    prompt = f"find a song that represents the emotions coming from this text: \"{text}\"\nsong title, artist | list of emotions | 2 keywords from text"
    return prompt


def get_OpenAI_analysis(query="", is_example_response=True, create_new_example=False):  # TODO: don't forget to turn off the example response
    """
    The get_OpenAI_analysis function takes a query and returns a response from the OpenAI model.
    The function takes in a user's query, and uses the OpenAI API to generate an analysis of that string which contains
    a song, sentiments and keywords

    :param query: Generate the prompt for the model
    :param is_example_response: Toggle between the local example response and the openai api
    :param create_new_example: Create a new example response from the openai api
    :return: A dictionary with three keys:
    """
    if not is_example_response:  # Later to be used as the main algorithm
        response = openai.Completion.create(
            model=config["model"],
            prompt=generate_prompt(query),
            temperature=config["temp"],
            top_p=config["top_p"],
            max_tokens=config["max_tokens"]
        )

        print(f"OpenAI Response: {response}")

        if create_new_example:  # Used only when a new example is desired
            with open(f"{EXAMPLE_PATH}/OpenAI_response_dict.txt", 'x') as response_file:
                response_file.write(json.dumps(response))

        return response

    with open(f"{EXAMPLE_PATH}/OpenAI_response_dict.txt", "r") as example_json:  # loads the example response locally
        response = json.load(example_json)

    return response

###############


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


def parse_OpenAI_response(response) -> dict:
    """
    The parse_OpenAI_response function takes in a response from the OpenAI API and parses it into a dictionary.
    The function first fetches the relevant text from the response, and then splits the text of the response by
    the constant seperator. The function then extracts these values using extract methods and returns them as a dictionary.

    :param response: Pass in the response from the api
    :return: A dictionary with the following keys:
    :doc-author: Trelent
    """

    total_text = response["choices"][0]["text"].split(RESPONSE_SEPERATOR)

    song_info = extract_song_title_and_artist(total_text[0].strip())  # title and artist
    prompt_sentiments = extract_sentiments(total_text[1].strip())  # sentiments
    prompt_keywords = extract_keywords(total_text[2].strip().strip('"'))  # keywords

    song_info.update(prompt_sentiments)
    song_info.update(prompt_keywords)

    return song_info


###############


### Main Method ###
def query_analysis(query: str):
    """
    The query_analysis function takes a string which is the user's mood (or story) description and returns a dictionary
    with the prompt analysis and song information.

    :param query:str: An input query provided by the user
    :return: A dictionary with prompt information (keywords and sentiment analysis) and song information (title and artist);
    """
    openAI_response = get_OpenAI_analysis(query=query)
    return parse_OpenAI_response(openAI_response)

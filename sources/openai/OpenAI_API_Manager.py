import os
import json
import openai
from openai.openai_object import OpenAIObject
import sources.openai.OpenAI_Config as OpenAI_Config
from dotenv import load_dotenv

#############
# CONSTANTS #
#############

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
EXAMPLE_PATH = "./api_managers/"
EXAMPLE_QUERY = "I just failed my last test and i dont know how things are going to turn out. im bumped and have zero energy"


###############


def get_OpenAI_analysis(query="", is_example_response=False,
                        create_new_example=False) -> OpenAIObject:  # TODO: don't forget to turn off the example response
    """
    The get_OpenAI_analysis function takes a query and returns a response from the OpenAI model.
    The function takes in a user's query, and uses the OpenAI API to generate an analysis of that string which contains
    a song, sentiments and keywords

    :param query: User's input text
    :param is_example_response: Toggle between the local example response and the openai api
    :param create_new_example: Create a new example response from the openai api
    :return: A dictionary with three keys:
    """
    config = OpenAI_Config.config
    if not is_example_response:  # Later to be used as the main algorithm
        response = openai.Completion.create(
            model=config["model"],
            prompt=generate_prompt(query=query),
            temperature=config["temp"],
            top_p=config["top_p"],
            max_tokens=config["max_tokens"],
            stop=config["stop"]
        )

        # print(f"OpenAI Response: {response}")

        if create_new_example:  # Used only when a new example is desired
            with open(f"{EXAMPLE_PATH}OpenAI_response_dict.txt", 'x') as response_file:
                response_file.write(json.dumps(response))

        return response

    with open(f"{EXAMPLE_PATH}OpenAI_response_dict.txt", "r") as example_json:  # loads the example response locally
        response = json.load(example_json)

    return response


def generate_prompt(query: str) -> str:
    """
    The generate_prompt function takes in a string of text entered by the user (his story) and returns a ready-to-use
    query for the OpenAI server to analyze

    :param query:str: Store the user's text (story) that will be used to generate a query
    :return: A string that will be used as a query for the openai server
    """
    prompt = f"\"{query}\"\n{OpenAI_Config.INPUT_SUFFIX}{OpenAI_Config.PROMPT_END_SUFFIX}"
    return prompt


################
# EXAMPLE RUNS #
################


# my_query = "My boyfriend told me we were going to the beach but instead he took me to Azrieli’s roof top where all our friends were waiting and proposed!! I’ve been waiting for this for four long years. I said NO."

# print(get_OpenAI_analysis(query=my_query, is_example_response=False, create_new_example=False))

# parsed_query = query_to_mooditem_dict(EXAMPLE_QUERY)
# my_song = SongAnalysis.create_song(title=parsed_query["title"], artist=parsed_query["artist"])
# print(my_song)

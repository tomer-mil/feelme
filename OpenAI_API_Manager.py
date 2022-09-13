import os
import json
from dotenv import load_dotenv
import openai
from OpenAI_Config import standard_config, finetuned_config
import Song_Analyzer

#############
# CONSTANTS #
#############

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
EXAMPLE_PATH = "/Users/tomermildworth/Desktop/Coding/FeelMe/feelme"
EXAMPLE_QUERY = "I just failed my last test and i dont know how things are going to turn out. im bumped and have zero energy"


###############


def get_OpenAI_analysis(prompt="", is_example_response=False, create_new_example=False):  # TODO: don't forget to turn off the example response
    """
    The get_OpenAI_analysis function takes a query and returns a response from the OpenAI model.
    The function takes in a user's query, and uses the OpenAI API to generate an analysis of that string which contains
    a song, sentiments and keywords

    :param prompt: Generate the prompt for the model
    :param is_example_response: Toggle between the local example response and the openai api
    :param create_new_example: Create a new example response from the openai api
    :return: A dictionary with three keys:
    """
    if not is_example_response:  # Later to be used as the main algorithm
        response = openai.Completion.create(
            model=finetuned_config["model"],
            prompt=prompt,
            temperature=finetuned_config["temp"],
            top_p=finetuned_config["top_p"],
            max_tokens=finetuned_config["max_tokens"],
            stop=finetuned_config["stop"]
        )

        print(f"OpenAI Response: {response}")

        if create_new_example:  # Used only when a new example is desired
            with open(f"{EXAMPLE_PATH}/OpenAI_response_dict.txt", 'x') as response_file:
                response_file.write(json.dumps(response))

        return response

    with open(f"{EXAMPLE_PATH}/OpenAI_response_dict.txt", "r") as example_json:  # loads the example response locally
        response = json.load(example_json)

    return response

################
# EXAMPLE RUNS #
################

# parsed_query = query_to_mooditem_dict(EXAMPLE_QUERY)
# my_song = SongAnalysis.create_song(title=parsed_query["title"], artist=parsed_query["artist"])
# print(my_song)
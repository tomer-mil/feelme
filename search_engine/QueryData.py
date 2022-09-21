from openai.openai_object import OpenAIObject
from sources.openai.OpenAI_API_Manager import get_OpenAI_analysis
from configs import Utils


def extract_sentiments(response_sentiments_text: str) -> dict:
    """
    The extract_sentiments function takes a string of comma-separated sentiments and returns a dictionary with the
    sentiments. The extract_sentiments function assumes that each sentiment in
    the input string is separated by a comma followed by a space. If there are multiple commas in the text or if
    there are no commas at all, then an empty dictionary will be returned.

    :param response_sentiments_text:str: Store the sentiments from the response of the api call
    :return: A dictionary with a list of strings as the value for the key "sentiments";
    """
    sentiments_list = response_sentiments_text.split(":")[1:]  # "\"emotions\": 3 emotions"
    sentiments_list[:] = [Utils.clean_word(word=sentiment) for sentiment in sentiments_list[0].split(", ")]
    # for sentiment in sentiments_list[0].split(", "):
    #     clean_word = Utils.clean_word(word=sentiment)
    #     clean_sentiments_list.append(clean_word)
    prompt_sentiments = {
        "sentiments": sentiments_list
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
    keywords_list = response_keywords_text.split(":")[1:]  # \"keywords\": 3 keywords
    keywords_list[:] = [Utils.clean_word(word=keyword) for keyword in keywords_list[0].split(", ")]

    prompt_keywords = {
        "keywords": keywords_list
    }
    return prompt_keywords


def extract_response_info(response_text: str) -> dict:
    responses_list = response_text.split("\n")

    sentiments_text, keywords_text = responses_list[-2], responses_list[-1]

    sentiments = extract_sentiments(response_sentiments_text=sentiments_text)
    keywords = extract_keywords(response_keywords_text=keywords_text)
    return {**sentiments, **keywords}


class QueryData:
    data = {
        "text": "",
        "sentiments": [],
        "keywords": []
    }

    def set_response_data(self, response: OpenAIObject):
        """
        The parse_OpenAI_response function takes in a response from the OpenAI API and parses it into a dictionary.
        The function first fetches the relevant text from the response, and then splits the text of the response by
        the constant seperator. The function then extracts these values using extract methods and returns them as a dictionary.

        :param response: Pass in the response from the api
        :return: A dictionary with the following keys:
        """

        response_data = extract_response_info(response_text=
                                              response["choices"][0]["text"])

        self.data.update(response_data)

    def __init__(self, query: str):
        openai_response = get_OpenAI_analysis(query=query)
        self.set_response_data(response=openai_response)
        self.data.update({"text": query})

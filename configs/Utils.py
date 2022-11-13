from urllib.parse import urlparse
from dotenv import find_dotenv

#####################
# GENERAL UTILITIES #
#####################

ENV_PATH = find_dotenv()

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


############################
# QUERY ANALYSIS UTILITIES #
############################

def clean_word(word: str) -> str:
    if not word.isalpha():
        word = word.replace(",", "").replace("-", " ")
        word = word.strip().strip(".").strip("(").strip(")").strip("!")
    return word.lower()

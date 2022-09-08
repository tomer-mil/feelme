from collections import namedtuple
from MoodVec import MoodVec
import pandas as pd
from Utils import clean_word

#############
# CONSTANTS #
#############

LEX_CSV_PATH = "/Users/tomermildworth/Desktop/Coding/FeelMe/feelme/lexicons/en/NRC-VAD-Lexicon_csv.csv"
DEFAULT_LANGUAGE = "en"

###########
# GLOBALS #
###########

global LEXICON
global QUERY_INFO_DICT

#############


def create_info_dict(text: str):
    """
    The create_info_dict function takes a string as input and sets the global dictionary with the following:
        - text: The original text that was passed in to be analyzed.
        - tokens: A dictionary containing the total number of tokens, the number of tokens in the lexicon,
            and average valence/energy scores for the text.
        - lang: The language of the given text
        - energy: Energy score for the text
        - valence: Valence score for the text
        - rating: The ratings of this analysis, calculated by ratio between total tokens and tokens in lexicon

    :param text:str: The text that is to be analyzed

    """
    global QUERY_INFO_DICT
    lang = detect_lang()
    QUERY_INFO_DICT = {
        "text": text,
        "tokens": {
            "total_tokens": 0,
            "tokens_in_lexicon": 0,
        },
        "lang": lang,
        "energy": 0.0,
        "valence": 0.0,
        "rating": 0.0
    }
    set_total_tokens()


def detect_lang():  # TODO: ADD RETURN TYPE. Build language detection engine
    """
    The detect_lang function takes the given text and returns its language encoding

    :return: Encoded language code
    """
    # TODO: lang_code = detect_language(text=QUERY_INFO_DICT["text"]), return lang_code.
    return DEFAULT_LANGUAGE


def set_total_tokens():
    """
    The set_total_tokens function sets the total number of tokens in the text.

    :return: None
    """
    QUERY_INFO_DICT["tokens"]["total_tokens"] = len(tokenize(QUERY_INFO_DICT["text"]))


#############


def set_mood_info():
    """
    The set_mood_info function sets the value of energy, valence and rating in the main dictionary

    :return None
    """
    calc_energy_valence()
    calc_rating()


def calc_energy_valence():
    """
    The calc_energy_valence function calculates and sets the energy and valence values in the main dictionary.
    Values are calculated by the average energy and valence across all tokens that appear in the lexicon.

    :return: None
    """
    totals_vec = calc_tokens_totals_vec(text=QUERY_INFO_DICT["text"])
    t_lex_tokens = QUERY_INFO_DICT["tokens"]["tokens_in_lexicon"]
    QUERY_INFO_DICT["energy"] = totals_vec.energy / t_lex_tokens
    QUERY_INFO_DICT["valence"] = totals_vec.valence / t_lex_tokens


def calc_rating():
    """
    The calc_rating function calculates the rating of a query by dividing the number of tokens in
    the lexicon by the total number of tokens. The result is stored in QUERY_INFO_DICT[&quot;rating&quot;].


    :return: The ratio of the number of tokens in the lexicon to the total number of tokens
    """
    rating = QUERY_INFO_DICT["tokens"]["tokens_in_lexicon"] / QUERY_INFO_DICT["tokens"]["total_tokens"]
    QUERY_INFO_DICT["rating"] = rating


def tokenize(text: str) -> list[str]:
    """
    The tokenize function takes a string as input and returns a list of tokens.
    The tokens are cleaned words from the text, with all punctuation removed.


    :param text:str: The text that needs to be tokenized
    :return: A list of words that have been cleaned

    """
    split_txt = text.split()
    for i in range(len(split_txt)):
        split_txt[i] = clean_word(word=split_txt[i])
    return split_txt


def cnt_token_in_lex():
    """
    The cnt_token_in_lex function increments the tokens_in_lexicon count by 1.

    :return: None

    """
    QUERY_INFO_DICT["tokens"]["tokens_in_lexicon"] += 1


def calc_tokens_totals_vec(text: str) -> MoodVec:
    """
    The calc_tokens_totals_vec function takes a string of text as input and returns a Mood_Vec object with the total
    energy and valence values for that text.
    The function first tokenizes the given text into individual words, then it checks if each word is in our lexicon.
    If so, it adds a count and calculates its mood values, Otherwise it generates an empty Mood_Vec object
    (energy and valence set to 0.0). Finally the mood values are summed and returned as a Mood_Vec.

    :param text:str: The text to be analyzed
    :return: A Mood_Vec object that contains the total energy and valence values of all tokens in the text
    """

    tokens_list = tokenize(text=text)
    prev_tokens = {}

    total_energy = 0.0
    total_valence = 0.0

    for token in tokens_list:

        if token in prev_tokens:
            if prev_tokens[token]["in_lex"]:
                cnt_token_in_lex()
            total_energy += prev_tokens[token]["mood_vec"].energy
            total_valence += prev_tokens[token]["mood_vec"].valence

        else:
            token_mood_vec = calc_token_mood_vec(token=token)
            token_in_lex = token_mood_vec is not None

            if not token_in_lex:
                token_mood_vec = MoodVec(energy=0.0, valence=0.0)
            else:
                cnt_token_in_lex()
            prev_tokens.update({
                token: {
                    "mood_vec": token_mood_vec,
                    "in_lex": token_in_lex
                }
            })

            total_energy += token_mood_vec.energy
            total_valence += token_mood_vec.valence

    return MoodVec(energy=total_energy, valence=total_valence)


def calc_token_mood_vec(token: str):
    """
    The calc_token_mood_vec function takes a token (a word) as input and returns a Mood_Vec for
    that token. If the token is not found in the lexicon, it returns None.

    :param token:str: Tokenized word from text
    :return: Mood_Vec for token; None if token is not in the lexicon

    """
    word_series = LEXICON[LEXICON["word"] == token]

    if word_series.empty:
        return None

    energy = float(word_series.iloc[0]["arousal"])
    valence = float(word_series.iloc[0]["valence"])

    return MoodVec(energy=energy, valence=valence)


#############


def load_lexicon() -> None:
    """
    The load_lexicon function loads the lexicon file with the query's language into a pandas dataframe.
    The function is called by the main() function and does not need to be used directly.

    :return: None
    """
    global LEXICON
    lang = QUERY_INFO_DICT["lang"]
    lex_path = set_lex_path(lang=lang)
    LEXICON = pd.read_csv(lex_path)


def set_lex_path(lang: str):  # TODO: ADD RETURN TYPE. We can add many languages so we have to choose the right one
    """
    The set_lex_path function sets the lexicon path for a given language.
    It takes one argument, lang, which is an encoded string representing the language of choice.
    The function returns the path to that particular lexicon.

    :param lang:str: Encoded language code string
    :return: The path to the lexicon csv file for a given language
    """
    return LEX_CSV_PATH


################
# MAIN METHODS #
################


def analyze_text(text: str) -> dict:
    """
    The get_analysis function takes a string as input and returns a dictionary of information about the text.
    The function first creates an info_dict, which is used to store all the information that will be returned.
    It then loads the lexicon into memory, so it can be referenced by other functions. It then calculates the
    energy and valence values of the text based on the lexicon. In addition the function rates the analysis.
    Finally, it returns a dictionary with the entire analysis data.

    :param text:str: The text that is to be analyzed
    :return: A dictionary of the query's mood analysis
    """
    create_info_dict(text=text)
    try:
        LEXICON
    except NameError:
        load_lexicon()
    set_mood_info()

    return QUERY_INFO_DICT


def multiple_texts_analysis(*args: str) -> list[dict]:
    """
    The multiple_texts_analysis function accepts a list of strings and returns a list of dictionaries,
    where each is an analysis of the given text.

    :param *args:str: Pass an arbitrary number of strings to the function
    :return: A list of dictionaries
    """
    analyzed_list = []

    for text in args:
        text_analysis = analyze_text(text=text)
        analyzed_list.append(text_analysis)

    return analyzed_list

from items.MoodVec import MoodVec
from search_engine.analyzers.Text_Analyzer import multiple_texts_analysis

#############
# CONSTANTS #
#############

QUERY_WEIGHT = 0.3
SENTIMENTS_WEIGHT = 0.7

#############


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

    return weighted_mood_vec(text_info=analyzed_texts[0], sentiments_info=analyzed_texts[1])

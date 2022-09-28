from items.Gif import Gif
from items.MoodItem import MoodItem
from sources.giphy.Giphy_API_Manager import get_gif_data_from_giphy
from search_engine.QueryData import QueryData
from search_engine.analyzers.MoodVec_Analyzer import calc_query_mood_vec
from items.Song import Song

from sources.db.Demo_50_songs_run import search_song_by_mood
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
    # song = search_song_by_mood(mood_v=text_mood_vec)  # TODO
    return text_mood_vec


#########################
# GIF SEARCHING METHODS #
#########################


def search_gif(keywords: list[str]) -> Gif:
    """
    The create_gif function takes a list of keywords and returns a Gif object.
    The function first creates the query string using the create_keywords_query function, then uses that query to search for gifs on giphy.com.
    It then takes the data from that search and creates a new Gif object with it's giphy id, keywords, and images.

    :param keywords:list: Pass in a list of keywords to be used
    :return: A gif object
    """

    gif_data = get_gif_data_from_giphy(keywords_list=keywords)

    new_gif = Gif(giphy_id=gif_data[0].get("id"),
                  keywords=" ,".join(keywords),
                  images=gif_data[0].get("images"))

    return new_gif


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
    query_data = QueryData(query=query)

    gif = search_gif(keywords=query_data.data["keywords"])
    song = search_song(text=query_data.data["text"], sentiments=query_data.data["sentiments"])
    example_song = Song(artist="artist", title="title", mood_vec=song)
    return MoodItem(song=example_song, gif=gif)


result = search(query="I got up really early. I wanted to go surf. It was difficult getting myself out of bed, and out of the house. I haven't had much sleep the last past nights but as soon as I saw the sea I was filled with joy and energy that helped me through my day")
print(result.song.mood_vec)
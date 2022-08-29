from authorization import auth_sp
from Song import Song

###############################
# CONSTANTS AND CONFIGURATION #
###############################
NUMBER_OF_SONGS = 1
sp = auth_sp  # Authorization's Spotify object


def get_track_info(title: str, artist: str):
    """
    The get_track_info function takes in a song title and artist name as strings,
    and returns the track's Spotify ID and URL.


    :param title:str: The name of the song
    :param artist:str: The artist name
    :return: A tuple containing the track id and the href of the track
    """
    query = f"{title} {artist}"
    track_paging = sp.search(query=query, limit=NUMBER_OF_SONGS)[0].items[0]  # tekore FullTrackPaging class
    return track_paging.id, track_paging.href


def get_mood_vec(track_ID: str):
    """
    The get_mood_vec function takes a track ID as input and returns the energy and valence values for that track.

    :param track_ID:str: The track's Spotify ID
    :return: A tuple containing the energy and valence values for a given track
    """
    track_audio_features = sp.track_audio_features(track_ID)
    return track_audio_features.energy, track_audio_features.valence


def create_song(title: str, artist: str):
    """
    The create_song function takes in a song title and artist,
    and returns a Song object with the corresponding Spotify ID,
    Spotify ID, title, artist name, and mood vector (energy-valence).


    :param title:str: The title of the song
    :param artist:str: The artist of the song
    :return: A song object
    """
    track_info = get_track_info(title=title, artist=artist)
    mood_vec = get_mood_vec(track_ID=track_info[0])
    return Song(spotify_ID=track_info[0], href=track_info[1],
                title=title, artist=artist,
                energy=mood_vec[0], valence=mood_vec[1])









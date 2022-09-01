import numpy as np
from numpy.linalg import norm
import pandas


def calc_dist(track_mood_vec, df):
    """
    The calc_dist function calculates the distance between a given track and all other tracks in the dataset.

    :param track_mood_vec: Calculate the distance between a track and all other tracks in the dataframe
    :param df: Calculate the distance between a track and all other tracks in the dataset
    :return: The distance between the track_mood_vec and each of the mood vectors in the dataframe
    """
    df["distances"] = df["mood_vec"].apply(lambda x: norm(track_mood_vec - np.array(x)))


def recommend(track_id, df, sp, n_recs):
    """
    The recommend function takes a track id, the dataframe of all tracks and their mood vectors,
    and Spotify's API object as arguments. It then uses the track_audio_features function from
    Spotify's API to get information about the suggested track (such as its valence and energy).
    It then creates a mood vector for that suggested track.
    The calc_dist function is called on this new mood vector along with all other tracks' in df.
    Finally, df is sorted by distance in ascending order (i.e., closest first) and only returns n recommendations.&quot;

    :param track_id: Get the track's information, which is used to create its mood vector
    :param df: Store the mood vectors of all tracks
    :param sp: Make api calls
    :param n_recs: Specify the number of recommendations that will be returned
    :return: A dataframe of the recommended tracks
    """
    # get suggested track's info and create its mood vec
    track_info = sp.track_audio_features(track_id)
    track_mood_vec = np.array(track_info.valence, track_info.energy)

    # calculate the distance between the track's mood vec and all other tracks
    calc_dist(track_mood_vec, df)

    # rearrange df by dist, in ascending order, and remove the same track
    df_sorted = df.sort_values(by="distances", ascending=True)

    return df_sorted.iloc[:n_recs]


import time
from sources.spotify.Authorization import authorize_try
from sources.spotify.User_Top_Items import hist_genres, get_top_artists, get_top_tracks

##############
# CONSTANTS #
##############
N_TRACKS_PER_GENRE = 100
N_GENRES = 20


spotify = authorize_try()
genres_hist = hist_genres()
# top_genres = list(genres_hist.keys())
all_genre_seed_list = spotify.recommendation_genre_seeds()
track_dict = {"id": [], "genre": [], "track_name": [], "artist_name": [], "valence": [], "energy": []}


def create_rec(rec_type: str):
    match rec_type:
        case "artists":
            top_artists = get_top_artists()
            for artist in top_artists:
                recs = spotify.recommendations(artist_ids=[artist.id])
        case "tracks":
            top_tracks = get_top_tracks()
            for item in top_tracks:
                recs = spotify.recommendations(track_ids=[item.id])
        case "genres":
            top_genres = list(hist_genres().keys())
            for genre in top_genres:
                recs = spotify.recommendations(genres=[genre])
        case _:
            recs = None

    recs = eval(
        recs.json().replace("null", "-999").replace("false", "False").replace("true", "True"))["tracks"]  # TODO: change replace to dumps, this is bad practice

    for item in recs:

        # ID and Genre
        track_dict["id"].append(item["id"])
        # track_dict["genre"].append(g)

        # Metadata
        track_meta = spotify.track(item["id"])
        track_dict["track_name"].append(track_meta.name)
        track_dict["artist_name"].append(track_meta.album.artists[0].name)

        # Valence and energy
        track_features = spotify.track_audio_features(item["id"])
        track_dict["valence"].append(track_features.valence)
        track_dict["energy"].append(track_features.energy)

        # Wait 0.2 seconds per track so that the api doesnt overheat
        time.sleep(0.2)
    return track_dict

##################
## PROCESS DATA ##
##################


# def rec_dict_to_df(data_dict):
#     # Store data in dataframe
#     df = pd.DataFrame(data_dict)
#
#     # Drop duplicates
#     df.drop_duplicates(subset="id", keep="first", inplace=True)
#     df.to_csv("valence_arousal_dataset_shelly.csv", index=False)
#
#     # Create mood vector and add it to the existing dataframe
#     df["mood_vec"] = df["valence", "energy"].values.tolist()


create_rec(rec_type="artists")

print(track_dict)

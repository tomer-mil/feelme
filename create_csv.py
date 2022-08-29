import time
import pandas as pd
from tqdm import tqdm
from authorization import auth_sp

sp = auth_sp

genres = sp.recommendation_genre_seeds()

N_RECS = 100

data_dict = {"id": [], "genre": [], "track_name": [], "artist_name": [],
             "valence": [], "energy": []}


def create_rec():
    for g in tqdm(genres):
        recs = sp.recommendations(genres=[g], limit=N_RECS)
        recs = eval(
            recs.json().replace("null", "-999").replace("false", "False").replace("true", "True"))["tracks"]  # TODO: change replace to dumps, this is bad practice

        for track in recs:

            # ID and Genre
            data_dict["id"].append(track["id"])
            data_dict["genre"].append(g)

            # Metadata
            track_meta = sp.track(track["id"])
            data_dict["track_name"].append(track_meta.name)
            data_dict["artist_name"].append(track_meta.album.artists[0].name)

            # Valence and energy
            track_features = sp.track_audio_features(track["id"])
            data_dict["valence"].append(track_features.valence)
            data_dict["energy"].append(track_features.energy)

            # Wait 0.2 seconds per track so that the api doesnt overheat
            time.sleep(0.2)

##################
## PROCESS DATA ##
##################


def rec_dict_to_df(data_dict):
    # Store data in dataframe
    df = pd.DataFrame(data_dict)

    # Drop duplicates
    df.drop_duplicates(subset="id", keep="first", inplace=True)
    df.to_csv("valence_arousal_dataset_tomer2.csv", index=False)

    # Create mood vector and add it to the existing dataframe
    df["mood_vec"] = df["valence", "energy"].values.tolist()

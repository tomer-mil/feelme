from authorization import authorize
from Song import Song

#############
# CONSTANTS #
#############
NUMBER_OF_SONGS = 1

sp = authorize()


def get_track_info(title: str, artist: str):
    query = f"{title} {artist}"
    track_paging = sp.search(query=query, limit=NUMBER_OF_SONGS)[0].items[0]
    track_id = track_paging.id
    href = track_paging.href
    return track_id, href


def get_mood_vec(track_ID: str):
    track_audio_features = sp.track_audio_features(track_ID)
    energy = track_audio_features.energy
    valence = track_audio_features.valence
    return energy, valence


def create_song(title: str, artist: str):
    track_info = get_track_info(title=title, artist=artist)
    mood_vec = get_mood_vec(track_ID=track_info[0])
    return Song(spotify_ID=track_info[0], href=track_info[1],
                title=title, artist=artist,
                energy=mood_vec[0], valence=mood_vec[1])









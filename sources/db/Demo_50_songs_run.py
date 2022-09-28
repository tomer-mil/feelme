from items.MoodVec import MoodVec
from sources.spotify.Authorization import authorize
from sources.spotify.User_Top_Items import get_top_tracks
from items.Song import Song
from sources.db.quadtree.Quadtree import Quadtree

sp = authorize()[0]
quadtree = Quadtree()

songs = []

top_tracks = get_top_tracks()

for track in top_tracks:

    track_energy = sp.track_audio_features(track_id=track.id).energy
    track_valence = sp.track_audio_features(track_id=track.id).valence

    mood_vec = MoodVec(energy=track_energy,
                       valence=track_valence)

    song = Song(title=track.name,
                artist=track.artists[0].name,
                spotify_ID=track.id,
                href=track.href,
                mood_vec=mood_vec
                )

    songs.append(song)
    quadtree.insert_data(data=song)

print(f"quad: {quadtree}")



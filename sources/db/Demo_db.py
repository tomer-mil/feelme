from items.MoodVec import MoodVec
from sources.spotify.Authorization import authorize
from sources.spotify.User_Top_Items import get_top_tracks
from items.Song import Song
from sources.db.quadtree2.Quadtree import Quadtree, NodeData, Point

sp = authorize()[0]
quadtree = Quadtree()

nodes = []

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

    new_point = Point(x=track_energy, y=track_valence)
    node = NodeData(position=new_point, data=song)

    nodes.append(node)
    quadtree.insert(node=node)

# print(quadtree)


# def search_song_by_mood(mood_v: MoodVec):
#     mood_point = Point(x=mood_v.energy, y=mood_v.valence)
#     return quadtree.nearest_point(point=mood_point)


mood = MoodVec(energy=0.6832794871794869, valence=0.8620384615384616)
# nearest_song = search_song_by_mood(mood_v=mood)

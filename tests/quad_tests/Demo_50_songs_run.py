from items.MoodVec import MoodVec
from sources.spotify.Authorization import authorize
from sources.spotify.User_Top_Items import get_top_tracks
from items.Song import Song
from sources.db.quadtree.Quadtree import Quadtree, Point
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import time
import datetime
import os

fig, ax = plt.subplots()

quadtree = Quadtree()


def create_csv_of_top_tracks():
    sp = authorize()[0]
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
        pd_formt_song = song.__dict__
        pd_formt_song.pop("mood_vec")
        pd_formt_song.update({
            "energy": mood_vec.energy,
            "valence": mood_vec.valence
        })
        songs.append(pd_formt_song)
    songs_df = pd.DataFrame(songs)
    songs_df.to_csv("tomer_top_50_songs.csv")


def load_songs_csv(path: str) -> list[Song]:
    songs_df = pd.read_csv(filepath_or_buffer=path)
    songs = []
    for i, pd_song in songs_df.iterrows():
        mood_vec = MoodVec(energy=pd_song["energy"], valence=pd_song["valence"])

        song = Song(title=pd_song["title"],
                    artist=pd_song["artist"],
                    spotify_ID=pd_song["spotify_ID"],
                    href=pd_song["href"],
                    mood_vec=mood_vec)

        songs.append(song)
    return songs


def draw_quad(quad: Quadtree, songs_list: list[Song], annotate: bool = False, show: bool = True):

    x_list = [SONG.mood_vec.energy for SONG in songs_list]
    y_list = [SONG.mood_vec.valence for SONG in songs_list]

    dpi = 600
    width, height = 1000, 1000

    plt.axis([0, 1, 0, 1])
    plt.xticks(np.arange(0, 1.125, step=0.125))
    plt.yticks(np.arange(0, 1.125, step=0.125))
    quad.draw(ax=ax)

    ax.scatter(x_list, y_list, s=3)

    if annotate:
        for i in range(len(x_list)):
            ax.annotate(f"({x_list[i]}, {y_list[i]})", (x_list[i], y_list[i]))

    if show:
        plt.show()


def add_search_points_to_drawing(rand_point: Point, closest_point: Point, candidates: list[Point]):
    points_line2d = []

    if rand_point:
        points_line2d.extend(plt.plot([rand_point.x], [rand_point.y],
                                      c='tab:red', marker='o'))

    if closest_point:
        points_line2d.extend(plt.plot([closest_point.x], [closest_point.y],
                                      c="tab:green", marker="*"))

    if len(candidates) > 0:
        for candidate in candidates:
            if closest_point != candidate.data.position:
                points_line2d.extend(plt.plot([candidate.data.position.x], [candidate.data.position.y],
                                              c="tab:purple", marker="$?$"))

    return points_line2d


def create_quad_from_csv(path: str = "", test: bool = False) -> list[Song]:
    if test:
        path = "/Users/tomermildworth/Desktop/Coding/FeelMe/feelme/tests/quad_tests/tomer_top_50_songs.csv"
    start_time = time.perf_counter()
    songs = load_songs_csv(path=path)
    for song in songs:
        quadtree.insert_data(data=song)
    end_time = time.perf_counter()
    print('Quadtree build time: {:6.7f} seconds for {:d} songs'.format(end_time - start_time, len(songs)))
    return songs


def points_from_csv(path: str) -> list[Point]:
    points_df = pd.read_csv(filepath_or_buffer=path)
    points = []

    for i, df_point in points_df.iterrows():
        point = Point(x=df_point["x"], y=df_point["y"])
        points.append(point)

    return points


def generate_test_directory():
    test_path = f"/Users/tomermildworth/Desktop/Coding/FeelMe/feelme/tests/quad_tests/{str(datetime.date.today())}"
    os.mkdir(path=test_path) if not os.path.exists(path=test_path) else None
    return test_path


def test_points(points=None, save_graphs: bool = True):
    songs_list = create_quad_from_csv(test=True)
    if points is None:
        points = np.random.rand(100, 2)

    draw_quad(quad=quadtree, songs_list=songs_list, annotate=False, show=False)
    test_path = generate_test_directory()

    total_search_time = 0.0

    for i, point in enumerate(points):
        test_point = Point(x=point[0], y=point[1]) if not isinstance(point, Point) else point

        start_time = time.perf_counter()
        closest_nodedata, candidates = quadtree.find_nearest_nodedata(point=test_point, with_candidates=True)

        end_time = time.perf_counter()

        total_search_time += (end_time - start_time)

        points_added = add_search_points_to_drawing(rand_point=test_point, closest_point=closest_nodedata.position, candidates=candidates)

        if save_graphs:
            plt.savefig(fname=f"{test_path}/{i}.png")

        for added_point in points_added:
            added_point.remove()

        print(f"i: {i}, Point: {test_point}, Closest NodeData: {closest_nodedata}")

    print('Total Search time build time: {:6.7f} seconds for {:d} points'.format(total_search_time, len(points)))


test_points(points=points_from_csv(path="/Users/tomermildworth/Desktop/Coding/FeelMe/feelme/tests/quad_tests/test_points_051022.csv"), save_graphs=True)

"""
i: 41, Point: 0.7568061690905719,0.8928003380588075, Closest NodeData: <(0.854, 0.844) | 15 Step by: Radiohead>
i: 15, Point: 0.6956626069585891,0.6380292344754412, Closest NodeData: <(0.695, 0.704) | מה שאתה רואה עכשיו by: Assaf Amdursky>
i: 18, Point: 0.34508705474659074,0.808907952068254, Closest NodeData: <(0.45, 0.951) | חשמל מהשמש by: Amir Lev>
i: 19, Point: 0.7649962342733603,0.5375325195438907, Closest NodeData: <(0.755, 0.637) | The Chain - 2004 Remaster by: Fleetwood Mac>
i: 21, Point: 0.49449193159931804,0.520798101221552, Closest NodeData: <(0.35, 0.525) | מונית צהובה by: Amir Lev>
i: 25, Point: 0.2528419339627974,0.3260676247874026, Closest NodeData: <(0.386, 0.348) | ג'וזפין by: Assaf Amdursky>
i: 26, Point: 0.9231277737297603,0.7482605969952697, Closest NodeData: <(0.798, 0.695) | Ain't No Fun (If the Homies Cant Have None) (feat. Nate Dogg, Warren G & Kurupt) by: Snoop Dogg>
i: 27, Point: 0.5484723909930188,0.6662223388498610, Closest NodeData: <(0.552, 0.783) | Hi, I'm Dave - From "DAVE" by: "DAVE">
i: 32, Point: 0.6930764132836135,0.6295354623137910, Closest NodeData: <(0.645, 0.595) | פלואו שנות אור by: Ori Shochat>
i: 33, Point: 0.9149504871172901,0.2862644117189313, Closest NodeData: <(0.68, 0.502) | קובי by: Dudu Faruk>
i: 34, Point: 0.29995597438033117,0.777330516222424, Closest NodeData: <(0.45, 0.951) | חשמל מהשמש by: Amir Lev>
i: 36, Point: 0.7620735746302721,0.0450359596424111, Closest NodeData: <(0.534, 0.256) | צל של תוכי by: Assaf Amdursky>
"""

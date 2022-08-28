from create_csv import sp
import tekore as tk
from authorization import CLIENT_ID, CLIENT_SECRET


# scope = tk.scope.user_top_read
# token = tk.prompt_for_user_token(sp, scope=scope)
# sp.playback_currently_playing()
# top_artists = sp.current_user_top_artists()
# print(top_artists)

import tekore as tk

redirect_uri = 'http://localhost/'
conf = (CLIENT_ID, CLIENT_SECRET, redirect_uri)
token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)

spotify = tk.Spotify(token)
tracks = spotify.current_user_top_tracks(limit=10)
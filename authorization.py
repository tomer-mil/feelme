import tekore as tk
from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')


# conf = tk.config_from_file("/Users/shellyrazinsky/PycharmProjects/feelme/.env")
# conf = (client_id, client_secret, redirect_uri)
# TODO: replace config_from_file to config_from_environment to get user's data (local)
# print(*conf)

# scope = tk.scope.user_top_read
# token = tk.prompt_for_user_token(*conf, 'user-top-read')

spotify = tk.Spotify('AQBl5KOuGAP-Trni7STXf53dLOKvIIiF56HKFK5YxyZNAXwDk_EnT5TKJkXVKHgwKpoRZ9RMS0VUp46rj4Ic99V39uUTKRzO0ST6Uu6C9azAUI8UIyv3ygboTgpsFOeuFzg')
artists = spotify.current_user_top_artists(limit=10)
print(artists)


def authorize():
    app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
    return tk.Spotify(app_token)


auth_sp = authorize()


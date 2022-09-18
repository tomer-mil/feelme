import tekore as tk
from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')


def authorize():
    app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
    return tk.Spotify(app_token)


auth_sp = authorize()


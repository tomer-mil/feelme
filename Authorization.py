import tekore as tk
from dotenv import load_dotenv
import os
from Utils import ENV_PATH

load_dotenv()
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')


def authorize():
    conf = tk.config_from_file(ENV_PATH, "SPOTIFY")  # Get required configuration from .env file
    cred = tk.Credentials(*conf)  # Client with configuration used to authorize a user
    spotify = tk.Spotify()
    return spotify, cred


auth_sp = authorize()
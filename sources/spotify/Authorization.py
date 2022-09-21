import tekore as tk
from dotenv import load_dotenv
import os
from configs.Utils import ENV_PATH

load_dotenv()
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')


def authorize() -> (tk.Spotify, tk.Credentials):
    """
    The authorize function is used to create a Spotify object and Credentials object.
    The Credentials object is then used to authorize the user, which returns an access token.
    This access token is then stored in the credentials file for later use.

    :return: A spotify object and a credentials object
    """
    conf = tk.config_from_file(ENV_PATH, "SPOTIFY")  # Get required configuration from .env file
    cred = tk.Credentials(*conf)  # Client with configuration used to authorize a user
    app_token = tk.request_client_token(*conf[:2])
    spotify = tk.Spotify(app_token)
    return spotify, cred


def authorize_try():
    app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
    return tk.Spotify(app_token)


def get_spotify() -> tk.Spotify:
    """
    The get_spotify function returns a Spotify object that is authorized to access the client's account.
    It does this by first checking if there is an existing token in the cache, and if not, it requests one from Spotify.

    :return: A Spotify object (from the tekore library)
    """
    return authorize()[0]

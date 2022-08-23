import tekore as tk

CLIENT_ID = '325ccd6336b34b64ab5953f2ccb224fa'
CLIENT_SECRET = '7579dbb156f9431c8a2dd7d0ef9b8113'

def authorize():
    app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
    return tk.Spotify(app_token)


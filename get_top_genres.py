import tekore as tk

client_id, client_secret, redirect_uri = tk.config_from_environment()

conf = tk.config_from_environment(return_refresh=True)
client_id, client_secret, redirect_uri, user_refresh = conf
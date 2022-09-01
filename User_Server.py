import tekore as tk

from flask import Flask, request, redirect, session

# https://developer.spotify.com/documentation/general/guides/authorization/code-flow/

###############################
# CONSTANTS AND CONFIGURATION #
###############################

in_link = '<a href="/login">login</a>'
out_link = '<a href="/logout">logout</a>'
login_msg = f'You can {in_link} or {out_link}'

SCOPES = [tk.scope.user_top_read]


conf = tk.config_from_file("/Users/tomermildworth/Desktop/Coding/FeelMe/feelme/.env", "Spotify")  # Get required configuration from .env file
cred = tk.Credentials(*conf)  # Client with configuration used to authorize a user
spotify = tk.Spotify()

###############################

auths = {}  # Ongoing authorisations: state -> UserAuth
users = {}  # User tokens: state -> token (use state as a user ID)

###############################


def app_factory() -> Flask:
    app = Flask(__name__)  # Creates the Flask server
    app.config['SECRET_KEY'] = 'aliens'  # Set SECRET_KEY in order to use flask's session https://flask.palletsprojects.com/en/2.2.x/api/#flask.session

    @app.route('/', methods=['GET'])  # When the URL goes to main page
    def main():

        print(f"auths: {auths} \nusers: {users}")

        # Checks if a user is already logged in with valid token
        user = session.get('user', None)
        token = users.get(user, None)

        # Return early if no login or old session
        if user is None or token is None:
            session.pop('user', None)
            return f'User ID: None<br>{login_msg}'

        page = f'User ID: {user}<br>{login_msg}'  # Main (login) page if user is found

        # Generate new Refresh_Token if current is about to expire
        if token.is_expiring:
            token = cred.refresh(token)
            users[user] = token

        try:
            with spotify.token_as(token):  # New Spotify item with current user's token by changing previous token
                playback = spotify.playback_currently_playing()  # User's "Now Playing"

            item = playback.item.name if playback else None
            page += f'<br>Now playing: {item}'
        except tk.HTTPError:
            page += '<br>Error in retrieving now playing!'

        return page

    @app.route('/login', methods=['GET'])  # User clicks "login"
    def login():

        if 'user' in session:  # If the user's credentials are known, i.e. saved in "session"
            return redirect('/', 307)  # Redirect back to main

        scope = SCOPES  # What scope to ask permission from the user
        auth = tk.UserAuth(cred, scope)  # Implement user authorisation flow. https://tekore.readthedocs.io/en/stable/reference/auth.html#tekore.UserAuth
        auths[auth.state] = auth  # Save current user's credentials in local 'auths' db
        return redirect(auth.url, 307)  # Navigate to Spotify's authorization page

    @app.route('/callback/', methods=['GET'])  # User accepts Spotify's authorization page
    def login_callback():

        # Get 'code' and 'state' arguments from URL sent after scope approval https://flask.palletsprojects.com/en/2.2.x/api/#flask.Request
        # args is an ImmutableMultiDict class (MultiDict is a datatype used to handle multiple values for the
        # same key) which implements every standard dictionary methods.
        code = request.args.get('code', None)  # 'code' is later used to get access token and Refresh_Token
        state = request.args.get('state', None)  # 'state' behaves as a local User_ID on the 'auths' db

        auth = auths.pop(state, None)  # Gets the local UserAuth object by the retrieved 'state' from 'auths' db

        # Checks if such 'state' (User_ID) was previously saved
        if auth is None:
            return 'Invalid state!', 400

        token = auth.request_token(code, state)  # Verify state consistency and request token using current user's UserAuth object. https://tekore.readthedocs.io/en/stable/reference/auth.html#tekore.UserAuth.request_token
        session['user'] = state  # Set new 'state' for user in session
        users[state] = token  # Set new token and Refresh_Token for current user
        return redirect('/', 307)  # Redirect back to main

    @app.route('/logout', methods=['GET'])
    def logout():
        uid = session.pop('user', None)
        if uid is not None:
            users.pop(uid, None)
        return redirect('/', 307)

    return app

# TODO: Make sure that "sessions" is the correct dict to fetch user's info WHEN MULTIPLE USERS ARE LOGGED IN (via ngrok)


def get_user_token() -> tk.Token:
    user = session.get('user', None)
    if user is None:
        raise ValueError("User not found")

    return users.get(user)


def get_user_id() -> str:
    user_id = session.get('user', None)
    if user_id is None:
        raise ValueError("User not found")


if __name__ == '__main__':
    application = app_factory()
    application.run('localhost', 8888)

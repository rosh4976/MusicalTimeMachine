import json
from spotipy.oauth2 import SpotifyOAuth

with open("keys.json") as f:
    keys = json.load(f)["spotify"]

CLIENT_ID = keys["client_id"]
CLIENT_SECRET = keys["client_secret"]
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "playlist-modify-private user-read-recently-played user-top-read"


sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    show_dialog=True
)

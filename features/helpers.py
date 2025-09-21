import spotipy
from flask import session

def get_spotify_client():
    token_info = session.get("token_info", None)
    if not token_info:
        return None
    return spotipy.Spotify(auth=token_info["access_token"])

def create_playlist(sp, name, description):
    return sp.user_playlist_create(
        user=session["user_id"],
        name=name,
        public=False,
        description=description
    )

from flask import session
import spotipy


def get_spotify_client():
    """Return a Spotify client using stored session token"""
    token_info = session.get("token_info", None)
    if not token_info:
        return None
    return spotipy.Spotify(auth=token_info["access_token"])

def create_playlist(sp, name, description):
    """Create a private playlist for the logged-in user"""
    return sp.user_playlist_create(
        user=session["user_id"],
        name=name,
        public=False,
        description=description
    )

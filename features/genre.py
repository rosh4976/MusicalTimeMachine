from flask import Blueprint, render_template, request, redirect, session, url_for
import spotipy
from utils import get_spotify_client, create_playlist

genre_bp = Blueprint("genre", __name__)

@genre_bp.route("/genre_page")
def genre_page():
    return render_template("genre.html")

@genre_bp.route("/genre", methods=["POST"])
def genre():
    genre = request.form["genre"]
    sp = get_spotify_client()
    if not sp:
        return redirect(url_for("auth.index"))

    query = f"{genre} music"
    result = sp.search(q=query, type="track", limit=20)
    uris = [item["uri"] for item in result["tracks"]["items"]]

    playlist = create_playlist(sp, f"{genre.capitalize()} Collection", f"{genre} based playlist")
    if uris:
        sp.playlist_add_items(playlist["id"], uris)

    return render_template("playlist.html", playlist=playlist)

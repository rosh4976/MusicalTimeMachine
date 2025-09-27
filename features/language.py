from flask import Blueprint, render_template, request, redirect, session, url_for
import spotipy
from utils import get_spotify_client, create_playlist

language_bp = Blueprint("language", __name__)

@language_bp.route("/language_page")
def language_page():
    return render_template("language.html")

@language_bp.route("/language", methods=["POST"])
def language():
    language = request.form["language"]
    sp = get_spotify_client()
    if not sp:
        return redirect(url_for("auth.index"))

    query = f"{language} music"
    result = sp.search(q=query, type="track", limit=20)
    uris = [item["uri"] for item in result["tracks"]["items"]]

    playlist = create_playlist(sp, f"{language.capitalize()} Hits", f"Best of {language} songs")
    if uris:
        sp.playlist_add_items(playlist["id"], uris)

    return render_template("playlist.html", playlist=playlist)

from flask import Blueprint, render_template, request, redirect, url_for
from utils import get_spotify_client, create_playlist

mood_bp = Blueprint("mood", __name__)

@mood_bp.route("/mood_page")
def mood_page():
    return render_template("mood.html")

@mood_bp.route("/mood", methods=["POST"])
def mood():
    mood = request.form["mood"]
    sp = get_spotify_client()
    if not sp:
        return redirect(url_for("auth.index"))

    mood_map = {
        "happy": "happy upbeat",
        "sad": "sad emotional",
        "chill": "relax calm",
        "party": "party dance"
    }
    query = mood_map.get(mood, "music")

    result = sp.search(q=query, type="track", limit=20)
    uris = [item["uri"] for item in result["tracks"]["items"]]

    playlist = create_playlist(sp, f"{mood.capitalize()} Vibes", f"A {mood} mood playlist")
    if uris:
        sp.playlist_add_items(playlist["id"], uris)

    return render_template("playlist.html", playlist=playlist)

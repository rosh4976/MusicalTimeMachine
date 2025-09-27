from flask import Blueprint, render_template, redirect, url_for
from utils import get_spotify_client, create_playlist

history_bp = Blueprint("history", __name__)

@history_bp.route("/history_page")
def history_page():
    return render_template("history.html")

@history_bp.route("/history", methods=["POST"])
def history():
    sp = get_spotify_client()
    if not sp:
        return redirect(url_for("auth.index"))

    results = sp.current_user_recently_played(limit=20)
    uris = [item["track"]["uri"] for item in results["items"]]

    playlist = create_playlist(sp, "Recently Played Mix", "Your recent listening history")
    if uris:
        sp.playlist_add_items(playlist["id"], uris)

    return render_template("playlist.html", playlist=playlist)


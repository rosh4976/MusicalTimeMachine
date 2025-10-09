# features/search.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils import get_spotify_client, create_playlist

search_bp = Blueprint("search", __name__)

@search_bp.route("/search_page")
def search_page():
    return render_template("search.html")

@search_bp.route("/search", methods=["POST"])
def search():
    q = request.form.get("query", "").strip()
    if not q:
        flash("Enter something to search")
        return redirect(url_for("search.search_page"))

    sp = get_spotify_client()
    if not sp:
        return redirect(url_for("auth.index"))

    res = sp.search(q=q, type="track", limit=50)
    tracks = res.get("tracks", {}).get("items", [])
    items = [{
        "id": t["id"],
        "name": t["name"],
        "artists": ", ".join([a["name"] for a in t["artists"]]),
        "uri": t["uri"],
        "preview_url": t.get("preview_url")
    } for t in tracks]

    return render_template("search_results.html", query=q, items=items)
@search_bp.route("/save_search", methods=["POST"])
def save_search():
    uris = request.form.getlist("uris")
    name = request.form.get("playlist_name", "Custom Search Playlist")
    description = request.form.get("playlist_desc", "")

    sp = get_spotify_client()
    if not sp:
        return redirect(url_for("auth.index"))

    playlist = create_playlist(sp, name, description)
    tracks = []

    if uris:
        for i in range(0, len(uris), 100):
            sp.playlist_add_items(playlist["id"], uris[i:i+100])
        tracks = [sp.track(uri) for uri in uris]

    return render_template(
        "playlist.html",
        playlist=playlist,
        tracks=tracks,
        added_count=len(uris)
    )

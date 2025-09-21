from flask import Blueprint, render_template, request, redirect, url_for
from features.helpers import get_spotify_client, create_playlist
import requests
from bs4 import BeautifulSoup
from utils import get_spotify_client, create_playlist


time_travel_bp = Blueprint("time_travel", __name__)


@time_travel_bp.route("/time_travel_page")
def time_travel_page():
    return render_template("time_travel.html")


@time_travel_bp.route("/time_travel", methods=["POST"])
def time_travel():
    date = request.form["date"]
    language = request.form["language"].lower()

    sp = get_spotify_client()
    if not sp:
        return redirect(url_for("auth.index"))

    year = date[:4]
    uris = []

    language_market = {
        "hindi": "IN",
        "tamil": "IN",
        "malayalam": "IN",
        "kannada": "IN",
        "telugu": "IN",
        "spanish": "ES",
        "korean": "KR",
        "japanese": "JP",
    }
    market = language_market.get(language, "US")

    if language == "english":
       
        url = f"https://www.billboard.com/charts/hot-100/{date}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        songs = [s.get_text(strip=True) for s in soup.select("li ul li h3")][:50]

        for song in songs:
            try:
                result = sp.search(q=f"track:{song} year:{year}", type="track", limit=1, market=market)
                if result and result["tracks"]["items"]:
                    uris.append(result["tracks"]["items"][0]["uri"])
            except Exception:
                continue
    else:
      
        playlist_query = f"{language} hits {year}"
        try:
            res = sp.search(q=playlist_query, type="playlist", limit=5, market=market)
            playlists = res.get("playlists", {}).get("items", []) if res else []
        except Exception:
            playlists = []

        for pl in playlists:
            if len(uris) >= 40:
                break
            pl_id = pl.get("id")
            if not pl_id:
                continue
            try:
                pl_items = sp.playlist_items(pl_id, fields="items.track.album.release_date,items.track.uri", limit=50)
            except Exception:
                pl_items = {}
            for it in pl_items.get("items", []):
                track = it.get("track")
                if not track:
                    continue
                rel = track.get("album", {}).get("release_date", "")
                rel_year = rel.split("-")[0] if rel else ""
                if rel_year == year or rel_year == "":
                    if track.get("uri") and track["uri"] not in uris:
                        uris.append(track["uri"])
                if len(uris) >= 40:
                    break

      
        if len(uris) < 20:
            track_query = f"{language} hits {year}"
            try:
                res = sp.search(q=track_query, type="track", limit=30, market=market)
                tracks = res.get("tracks", {}).get("items", []) if res else []
            except Exception:
                tracks = []
            for item in tracks:
                rel = item.get("album", {}).get("release_date", "")
                rel_year = rel.split("-")[0] if rel else ""
                if rel_year == year or rel_year == "":
                    if item.get("uri") and item["uri"] not in uris:
                        uris.append(item["uri"])
                if len(uris) >= 40:
                    break

    playlist = create_playlist(
        sp,
        f"{language.capitalize()} Hits - {date}",
        f"Top {language} songs from {date}"
    )

    if uris:
       
        for i in range(0, len(uris), 100):
            sp.playlist_add_items(playlist["id"], uris[i:i+100])
        return render_template("playlist.html", playlist=playlist, added_count=len(uris))
    else:
        return render_template(
            "playlist.html",
            playlist=playlist,
            added_count=0,
            message="⚠️ No matching songs found for this language/date. Try another year or language."
        )

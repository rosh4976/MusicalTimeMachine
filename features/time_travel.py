from flask import Blueprint, render_template, request, redirect, url_for
from utils import get_spotify_client, create_playlist
import requests
from bs4 import BeautifulSoup

time_travel_bp = Blueprint("time_travel", __name__)

def get_billboard_hot_100(year, max_songs=50):
    """Scrape Billboard Hot 100 for Dec 31 of given year"""
    url = f"https://www.billboard.com/charts/hot-100/{year}-12-31"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    songs = [s.get_text(strip=True) for s in soup.select("li ul li h3")]
    return songs[:max_songs]


def fetch_tracks(sp, query, year, market="US", max_songs=50):
    """Search Spotify in multiple batches and filter by year"""
    uris = []
    for offset in range(0, 200, 50): 
        results = sp.search(q=query, type="track", limit=50, offset=offset, market=market)
        for item in results["tracks"]["items"]:
            release_date = item["album"].get("release_date", "")
            release_year = release_date.split("-")[0] if release_date else ""
            if release_year == year and item["uri"] not in uris:
                uris.append(item["uri"])
            if len(uris) >= max_songs:
                return uris
    return uris


@time_travel_bp.route("/time_travel_page")
def time_travel_page():
    return render_template("time_travel.html")


@time_travel_bp.route("/time_travel", methods=["POST"])
def time_travel():
    year = request.form["year"]
    language = request.form["language"].lower()
    song_count = int(request.form.get("song_count", 30))  
    source = request.form.get("source", "spotify")        

    sp = get_spotify_client()
    if not sp:
        return redirect(url_for("auth.index"))

    uris = []

    language_market = {
        "hindi": "IN",
        "tamil": "IN",
        "malayalam": "IN",
        "telugu": "IN",
        "kannada": "IN",
        "spanish": "ES",
        "korean": "KR",
        "japanese": "JP",
        "english": "US"
    }
    market = language_market.get(language, "US")

    if language == "english":
        if source == "billboard":
            songs = get_billboard_hot_100(year, max_songs=song_count)
            for song in songs:
                try:
                    result = sp.search(q=f"track:{song} year:{year}", type="track", limit=1, market="US")
                    if result and result["tracks"]["items"]:
                        uris.append(result["tracks"]["items"][0]["uri"])
                except Exception:
                    continue
        else: 
            query = f"english hits {year}"
            uris = fetch_tracks(sp, query, year, "US", max_songs=song_count)

    else:
       
        query = f"{language} hits {year}"
        uris = fetch_tracks(sp, query, year, market, max_songs=song_count)

       
        if len(uris) < song_count // 2:
            alt_query = f"{language} top songs {year}"
            extra = fetch_tracks(sp, alt_query, year, market, max_songs=song_count - len(uris))
            uris.extend(extra)

    playlist = create_playlist(
        sp,
        f"{language.capitalize()} Hits - {year}",
        f"Top {language} songs released in {year}"
    )

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
    else:
    
     return render_template(
        "playlist.html",
        playlist=playlist,
        tracks=[], 
        added_count=0,
        message=f"⚠️ No matching {language} songs found for {year}. Try another year."
    )

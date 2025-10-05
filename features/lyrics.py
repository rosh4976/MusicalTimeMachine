from flask import Blueprint, render_template, request, redirect, url_for
import requests

lyrics_bp = Blueprint("lyrics", __name__, url_prefix="/lyrics")


@lyrics_bp.route("/lyrics_page")
def lyrics_page():
    return render_template("lyrics.html")


@lyrics_bp.route("/lyrics", methods=["POST"])
def lyrics():
    artist = request.form.get("artist")
    song = request.form.get("song")


    try:
        url = f"https://api.lyrics.ovh/v1/{artist}/{song}"
        response = requests.get(url)
        data = response.json()
        lyrics_text = data.get("lyrics", "Lyrics not found 😢")
    except Exception:
        lyrics_text = "Error fetching lyrics."

    return render_template("lyrics_result.html", artist=artist, song=song, lyrics=lyrics_text)

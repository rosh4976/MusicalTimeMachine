from flask import Blueprint, render_template, session, redirect, url_for
from utils import get_spotify_client

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/")
def dashboard():
    if "token_info" not in session:
        return redirect(url_for("auth.index"))

    sp = get_spotify_client()
    if not sp:
        return redirect(url_for("auth.index"))

   
    try:
        top_tracks = sp.current_user_top_tracks(limit=10, time_range="short_term")
        top_artists = sp.current_user_top_artists(limit=5, time_range="short_term")
        recently_played = sp.current_user_recently_played(limit=50)

        stats = {
            "songs_this_week": len(recently_played["items"]) if recently_played else 0,
            "top_artist": top_artists["items"][0]["name"] if top_artists and top_artists["items"] else "Unknown"
        }
    except Exception as e:
        print("⚠️ Error fetching dashboard stats:", e)
        stats = {"songs_this_week": 0, "top_artist": "Unknown"}

    return render_template("dashboard.html", user_name=session.get("user_name", "Guest"), stats=stats)

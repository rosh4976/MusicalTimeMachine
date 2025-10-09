from flask import Blueprint, render_template, session, redirect, url_for
from utils import get_spotify_client
from datetime import datetime, timedelta, timezone
from collections import Counter

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/")
def dashboard():
    if "token_info" not in session:
        return redirect(url_for("auth.index"))

    sp = get_spotify_client()
    if not sp:
        return redirect(url_for("auth.index"))

    try:
        # Fetch recent plays and top artists
        recently_played = sp.current_user_recently_played(limit=50)
        top_artists = sp.current_user_top_artists(limit=5, time_range="short_term")

        # ✅ Calculate songs actually played within the last 7 days
        now = datetime.now(timezone.utc)
        week_ago = now - timedelta(days=7)

        played_dates = []
        for item in recently_played.get("items", []):
            played_at = datetime.fromisoformat(item["played_at"].replace("Z", "+00:00"))
            if played_at > week_ago:
                played_dates.append(played_at.date().isoformat())

        # Count songs per day
        date_counts = Counter(played_dates)
        today = datetime.now().date()
        labels = [(today - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
        weekly_counts = [date_counts.get(day, 0) for day in labels]

        # Top artist names + popularity (for bar chart)
        artist_labels = [a["name"] for a in top_artists.get("items", [])]
        artist_counts = [a["popularity"] for a in top_artists.get("items", [])]

        # Dashboard stats summary
        stats = {
            "songs_this_week": len(played_dates),
            "top_artist": artist_labels[0] if artist_labels else "Unknown",
            "weekly_labels": labels,
            "weekly_counts": weekly_counts,
            "artist_labels": artist_labels,
            "artist_counts": artist_counts,
        }

    except Exception as e:
        print("⚠️ Error fetching dashboard stats:", e)
        stats = {
            "songs_this_week": 0,
            "top_artist": "Unknown",
            "weekly_labels": [],
            "weekly_counts": [],
            "artist_labels": [],
            "artist_counts": [],
        }

    return render_template(
        "dashboard.html",  
        user_name=session.get("user_name", "Guest"),
        stats=stats
    )

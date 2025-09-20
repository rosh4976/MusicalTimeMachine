from flask import Blueprint, redirect, render_template, request, session, url_for
import spotipy
import glob, os
from config import sp_oauth

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def index():
    return render_template("index.html")

@auth_bp.route("/login")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@auth_bp.route("/callback")
def callback():
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code, as_dict=True)
    session["token_info"] = token_info

    sp = spotipy.Spotify(auth=token_info["access_token"])
    user = sp.current_user()
    session["user_id"] = user["id"]
    session["user_name"] = user["display_name"]

    return redirect(url_for("dashboard.dashboard"))

@auth_bp.route("/logout")
def logout():
    session.clear()
    for f in glob.glob(".cache*"):
        os.remove(f)
    return render_template("logout.html")

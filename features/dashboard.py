from flask import Blueprint, render_template, session, redirect, url_for

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    if "token_info" not in session:
        return redirect(url_for("auth.index"))
    return render_template("dashboard.html", user_name=session["user_name"])

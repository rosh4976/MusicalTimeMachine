from flask import Flask
from features.auth import auth_bp
from features.dashboard import dashboard_bp
from features.time_travel import time_travel_bp
from features.mood import mood_bp


app = Flask(__name__)
app.secret_key = "supersecretkey" 


app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
app.register_blueprint(time_travel_bp, url_prefix="/time_travel")
app.register_blueprint(mood_bp, url_prefix="/mood")



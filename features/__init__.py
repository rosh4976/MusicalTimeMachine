from .auth import auth_bp
from .dashboard import dashboard_bp
from .time_travel import time_travel_bp
from .mood import mood_bp



all_blueprints = [
    auth_bp,
    dashboard_bp,
    time_travel_bp,
    mood_bp,
   
]

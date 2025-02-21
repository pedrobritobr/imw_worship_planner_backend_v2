from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.router import user_routes, planner_routes, church_routes

def create_app():
    app = Flask(__name__)
    config = Config()
    app.config.from_object(config)

    CORS(app)

    app.json.ensure_ascii=False

    app.register_blueprint(user_routes, url_prefix="/user")
    app.register_blueprint(planner_routes, url_prefix="/planner")
    app.register_blueprint(church_routes, url_prefix="/church")

    return app

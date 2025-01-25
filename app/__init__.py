from flask import Flask
from flask_cors import CORS
from app.config import Config

def create_app():
    app = Flask(__name__)
    CORS(app)

    config = Config()
    config.validate()
    app.config.from_object(config)
    app.json.ensure_ascii=False

    from app.router import user_routes, planner_routes
    app.register_blueprint(user_routes, url_prefix="/user")
    app.register_blueprint(planner_routes, url_prefix="/planner")

    return app

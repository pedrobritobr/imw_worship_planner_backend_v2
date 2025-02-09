from flask import Flask
from flask_cors import CORS

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers.config import Config
from router import user_routes, planner_routes

app = Flask(__name__)
config = Config()
config.validate()
app.config.from_object(config)

CORS(app)

app.json.ensure_ascii=False

app.register_blueprint(user_routes, url_prefix="/user")
app.register_blueprint(planner_routes, url_prefix="/planner")

@app.route('/')
def home():
    print('Hello World')
    return '@pedrobritobr'

if __name__ == "__main__":
    app.run(debug=True)

from flask import Blueprint, jsonify
from app.validations import phrase_authentication, validate_token

from app.service.BigQueryService import BigQueryService

planner_routes = Blueprint("planner", __name__)

@planner_routes.route("/", methods=["GET"])
@phrase_authentication
@validate_token
def get_planners(user):
    try:
        email = user.get("email")
        planner = BigQueryService().get_planner(email)
        print(f"{planner =}")

        return jsonify({"message": "Lista de planners"})
    except Exception as error:
        return jsonify({"error": str(error)}), 500
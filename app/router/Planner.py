from flask import Blueprint, jsonify

planner_routes = Blueprint("planner", __name__)

@planner_routes.route("/", methods=["GET"])
def get_planners():
    return jsonify({"message": "Lista de planners"})

from flask import Blueprint, jsonify, request
import pandas as pd

from app.validations import phrase_authentication, validate_token
from app.service.BigQueryService import BigQueryService, PlannerNotFoundException
from app.helpers import normalize_df

planner_routes = Blueprint("planner", __name__)

@planner_routes.route("/", methods=["GET"])
@phrase_authentication
@validate_token
def get_planner(user):
    try:
        email = user.get("email")

        if not email:
            return jsonify({"message": "Usuário não autenticado."}), 401

        planner = BigQueryService().get_planner(email)
        planner = {
            "activities": planner["planner_activities"],
            "selectedDate": planner["planner_selectedDate"],
            "ministerSelected": planner["planner_ministerSelected"],
            "worshipTitle": planner["planner_worshipTitle"],
            "churchName": planner["planner_churchName"],
            "creator": {
                "name": planner["user_name"],
                "email": planner["user_email"],
                "church": planner["user_church"]
            }
        }

        return jsonify(planner), 200
    except PlannerNotFoundException as error:
        return jsonify({"message": "Nenhum cronograma encontrado."}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@planner_routes.route("/", methods=["POST"])
@phrase_authentication
@validate_token
def create_planner(user):
    try:
        data = request.json.get('data')

        if not data:
            return jsonify({"message": "Cronograma não foi recebido."}), 400
        flattened_data = {
            "planner_activities": data.get("activities"),
            "planner_selectedDate": data.get("selectedDate"),
            "planner_ministerSelected": data.get("ministerSelected"),
            "planner_worshipTitle": data.get("worshipTitle"),
            "planner_churchName": data.get("churchName"),
            "user_name": user.get("name"),
            "user_email": user.get("email"),
            "user_church": user.get("church")
        }

        ids_on_empty_planner = ["firstActivity", "lastActivity"]
        activities_id = [activity["id"] for activity in flattened_data["planner_activities"]]

        if set(ids_on_empty_planner) == set(activities_id):
            return jsonify({"message": "Cronograma vazio."}), 400

        df = pd.DataFrame([flattened_data])
        df = normalize_df(df)
        BigQueryService().record_planner(df)
        return '', 201

    except Exception as error:
        return jsonify({"error": str(error)}), 500

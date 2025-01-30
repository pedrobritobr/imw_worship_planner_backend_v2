from flask import Blueprint, jsonify, request
import pandas as pd
import json

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
            "activities": json.loads(planner["planner_activities"]),
            "selectedDate": planner["planner_selectedDate"],
            "ministerSelected": planner["planner_ministerSelected"],
            "worshipTitle": planner["planner_worshipTitle"],
            "creator": {
                "name": planner["user_name"],
                "email": planner["user_email"],
                "church": planner["user_church"]
            }
        }
        return jsonify(planner), 200
    except PlannerNotFoundException as error:
        print(error)
        return jsonify({"message": "Nenhum cronograma encontrado."}), 404
    except Exception as error:
        print(error)
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
            "user_name": data["user"]["name"],
            "user_email": data["user"]["email"],
            "user_church": data["user"]["church"],
            "planner_activities": data["planner"]["activities"],
            "planner_selectedDate": data["planner"]["selectedDate"],
            "planner_ministerSelected": data["planner"]["ministerSelected"],
            "planner_worshipTitle": data["planner"]["worshipTitle"]
        }

        print(f"{flattened_data['planner_selectedDate']}")
        print(f"{flattened_data['planner_ministerSelected']}")
        print(f"{flattened_data['planner_worshipTitle']}")

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

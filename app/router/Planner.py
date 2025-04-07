from flask import Blueprint, jsonify, request
import pandas as pd

from app.validations import phrase_authentication, validate_token
from app.service.BigQueryService import BigQueryService, PlannerNotFoundException
from app.helpers import normalize_df, nested_planner

planner_routes = Blueprint("planner", __name__)

@planner_routes.route("/", methods=["GET"])
@phrase_authentication
@validate_token
def get_planner(user):
    try:
        email = user.get("email")

        if not email:
            return jsonify({"error": "Usuário não autenticado."}), 401

        planner = BigQueryService().get_planner(email)
        planner = nested_planner(planner)

        return jsonify(planner), 200
    except PlannerNotFoundException as error:
        return jsonify({"error": "Nenhum cronograma encontrado."}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@planner_routes.route("/<planner_id>", methods=["GET"])
@phrase_authentication
@validate_token
def get_planner_by_id(user, planner_id):
    try:
        email = user.get("email")

        if not email:
            return jsonify({"error": "Usuário não autenticado."}), 401

        planner = BigQueryService().get_planner_by_id(planner_id)
        planner = nested_planner(planner)

        return jsonify(planner), 200
    except PlannerNotFoundException as error:
        return jsonify({"error": f"Cronograma não encontrado | ID:{planner_id}"}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@planner_routes.route("/", methods=["POST"])
@phrase_authentication
@validate_token
def create_planner(user):
    try:
        data = request.json.get('data')

        if not data:
            return jsonify({"error": "Cronograma não foi recebido."}), 400

        flattened_data = {
            "planner_id": data.get("id"),
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
            return jsonify({"error": "Cronograma vazio."}), 400

        df = pd.DataFrame([flattened_data])
        df = normalize_df(df)
        BigQueryService().record_planner(df)
        return '', 201

    except Exception as error:
        return jsonify({"error": str(error)}), 500

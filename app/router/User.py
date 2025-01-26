from flask import Blueprint, jsonify, current_app
from flask import request
import re
from datetime import datetime
import pytz
from app.validations import phrase_authentication, is_valid_email, is_valid_password
from app.security import hash_password, validate_password, generate_jwt

from app.service.BigQueryService import BigQueryService

user_routes = Blueprint("user", __name__)

@user_routes.route("/login", methods=["POST"])
@phrase_authentication
def login():
    try:
        data = request.get_json()
    except Exception as error:
        return jsonify({"error": "Payload inválido"}), 400

    email = data.get("email")
    password = data.get("password")

    values = [ email, password ]

    if not all(values):
        return jsonify({"error": "Todos os campos são obrigatórios. [name, email, password, church]"}), 400

    if not is_valid_email(email):
        return jsonify({"error": "Email inválido"}), 400

    if not is_valid_password(password):
        return jsonify({"error": "A senha deve ter pelo menos 8 caracteres"}), 400

    try:
        user = BigQueryService().get_user(email)
    except Exception as error:
        return jsonify({"error": f"Erro no login. {error}"}), 500

    check_password = validate_password(user["password"], password)
    if not check_password:
        return jsonify({"error": "Senha inválida"}), 401

    user.pop("password")
    user.pop("tsIngestion")

    token = generate_jwt(user)
    return jsonify({"message": token})

@user_routes.route("/", methods=["POST"])
@phrase_authentication
def create_user():
    try:
        data = request.get_json()
    except Exception as error:
        return jsonify({"error": "Payload inválido"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    church = data.get("church")

    values = [name, email, password, church]

    if not all(values):
        return jsonify({"error": "Todos os campos são obrigatórios. [name, email, password, church]"}), 400

    if not is_valid_email(email):
        return jsonify({"error": "Email inválido"}), 400

    if not is_valid_password(password):
        return jsonify({"error": "A senha deve ter pelo menos 8 caracteres"}), 400

    hashed_password = hash_password(password)

    user_dict = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "church": church,
        "tsIngestion": datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        BigQueryService().record_user([user_dict])
    except Exception as error:
        return jsonify({"error": f"Erro ao criar usuário. {error}"}), 500

    return jsonify({"message": user_dict})

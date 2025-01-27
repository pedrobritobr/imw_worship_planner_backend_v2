from flask import Blueprint, jsonify
from flask import request
from datetime import datetime
import pytz
from app.validations import phrase_authentication, is_valid_email, is_valid_password
from app.security import hash_password, validate_password, generate_jwt

from app.service.BigQueryService import BigQueryService, UserNotFoundException

user_routes = Blueprint("user", __name__)

@user_routes.route("/login", methods=["POST"])
@phrase_authentication
def login():
    try:
        data = request.get_json()
    except Exception as error:
        return jsonify({"error": "Ocorreu um erro inesperado. Tente novamente mais tarde."}), 400

    email = data.get("email")
    password = data.get("password")

    values = [ email, password ]

    if not all(values):
        return jsonify({"error": "Todos os campos são obrigatórios."}), 400

    if not is_valid_email(email):
        return jsonify({"error": "Email inválido."}), 400

    if not is_valid_password(password):
        return jsonify({"error": "A senha deve ter pelo menos 8 caracteres."}), 400

    try:
        user = BigQueryService().get_user(email)
    except UserNotFoundException as error:
        return jsonify({"error": "Usuário não cadastrado."}), 404
    except Exception as error:
        return jsonify({"error": "Ocorreu um erro inesperado. Tente novamente mais tarde."}), 500

    check_password = validate_password(user["password"], password)
    if not check_password:
        return jsonify({"error": "Senha inválida."}), 401

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
        return jsonify({"error": "Ocorreu um erro inesperado. Tente novamente mais tarde."}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    church = data.get("church")

    values = [name, email, password, church]

    if not all(values):
        return jsonify({"error": "Todos os campos são obrigatórios."}), 400

    if not is_valid_email(email):
        return jsonify({"error": "Email inválido."}), 400

    if not is_valid_password(password):
        return jsonify({"error": "A senha deve ter pelo menos 8 caracteres."}), 400

    hashed_password = hash_password(password)

    user_dict = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "church": church,
        "tsIngestion": datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        bigquery = BigQueryService()

        try:
            bigquery.get_user(email)
            return jsonify({"error": "O email já cadastrado."}), 400
        except UserNotFoundException:
            bigquery.record_user([user_dict])
    except Exception as error:
        return jsonify({"error": f"Erro ao cadastrar usuário."}), 500

    user_dict.pop("password")
    user_dict.pop("tsIngestion")

    token = generate_jwt(user_dict)
    return jsonify({"message": token})

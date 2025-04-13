from flask import Blueprint, jsonify, request
import uuid
from datetime import datetime
import pytz

from app.service.CloudStorageService import CloudStorage
from app.service.BigQueryService import BigQueryService
from app.validations import phrase_authentication, validate_token
from app.helpers import sanitize_email

feedback_routes = Blueprint("feedback", __name__)

@feedback_routes.route("/", methods=["POST"])
@phrase_authentication
@validate_token
def get_feedback(user):
    try:
        user_email = user.get("email")
        user_email = sanitize_email(user_email)

        form_data = request.form
        files_data = request.files

        feedback_id = str(uuid.uuid4())
        feedback_text = form_data.get('feedbackText', '')

        cloud_storage = CloudStorage()

        folder_name = f"{user_email}/{feedback_id}"
        image_urls, errors = cloud_storage.upload_feedback_files(files_data, folder_name)

        if not image_urls and len(errors) == len(files_data):
            return jsonify({"error": "Nenhum arquivo enviado."}), 400

        try:
            feedback_dict = {
                "feedback_id": feedback_id,
                "feedback_text": feedback_text,
                "user_email": user_email,
                "image_urls": image_urls,
                "errors": errors,
                "tsIngestion": datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S")
            }

            BigQueryService().record_feedback(feedback_dict)
        except Exception as error:
            cloud_storage.delete_folder(folder_name)
            return jsonify({"error": str(error)}), 500

        if errors:
            response = {
                "message": "Feedback recebido com sucesso, mas alguns arquivos falharam ao serem enviados.",
                "error": [f"Erro ao fazer upload do arquivo {error['file']}" for error in errors]
            }
            return jsonify(response), 207
        return jsonify({"message": "Feedback recebido com sucesso!"}), 200

    except Exception as error:
        return jsonify({"error": str(error)}), 500

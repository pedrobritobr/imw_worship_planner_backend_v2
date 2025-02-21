from flask import Blueprint, jsonify

from app.service.BigQueryService import BigQueryService, NoChurchFoundException
from app.validations import phrase_authentication
from app.helpers import capitalize_words, deduplicate_by_similarity

church_routes = Blueprint("church", __name__)

@church_routes.route("/", methods=["GET"])
@phrase_authentication
def get_churches():
    try:
        churches = BigQueryService().get_churches()
        churches = [church["church"] for church in churches]
        churches = deduplicate_by_similarity(churches)
        churches = [capitalize_words(church) for church in churches]

        return jsonify(churches), 200
    
    except NoChurchFoundException as error:
        return jsonify({"error": "Nenhuma igreja cadastrada."}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 500

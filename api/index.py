from flask import Flask, request, jsonify
from datetime import datetime
import pytz

from get_envs import PROJECT_ID, DATASET_ID, TABLE_ID, TABLE_AMBIENT

app = Flask(__name__)

# def insert_data(data):
#     # Substitua esta função pela lógica para inserir os dados no banco de dados
#     pass

# def error_logging(res, error):
#     # Substitua esta função pela lógica de registro de erros
#     return res.status_code, jsonify({"message": str(error)})

# @app.route('/planner', methods=['POST'])
# def planner():
#     try:
#         if request.headers.get('keyword') != PLANNER_PHRASE:
#             return jsonify({"message": "Unauthorized"}), 401

#         planner = request.json.get('planner')

#         if not planner:
#             return jsonify({"message": "Cronograma não recebido."}), 400

#         tz = pytz.timezone('America/Sao_Paulo')
#         new_data = {
#             "planner": str(planner),
#             "tsIngestion": datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
#         }

#         insert_data(new_data)
#         return '', 201

#     except Exception as error:
#         return error_logging(jsonify({"message": "Internal Server Error"}), error)

@app.route('/')
def home():
    return 'About'

@app.route('/about')
def about():
    return f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}{TABLE_AMBIENT}"

if __name__ == '__main__':
    app.run(debug=True)

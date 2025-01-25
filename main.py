from app import create_app

app = create_app()

@app.route('/')
def home():
    return '@pedrobritobr'

if __name__ == "__main__":
    app.run(debug=True)

# from flask import Flask, request, jsonify
# from datetime import datetime
# import pytz
# import pandas as pd

# import sys
# import os
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# from backend.api.config import PROJECT_ID, DATASET_ID, TABLE_ID, TABLE_AMBIENT, PLANNER_PHRASE

# app = Flask(__name__)


# def error_logging(error):
#     print(f"Error: {error}")
#     return jsonify({"message": "Internal error."}), 500

# def normalize_df(df):
#     df["planner_selectedDate"] = pd.to_datetime(df["planner_selectedDate"]).dt.date
#     df["planner_activities"] = df["planner_activities"].apply(
#         lambda activities: [
#             {**activity, "duration": int(activity["duration"])} for activity in activities
#         ]
#     )
 
#     tz = pytz.timezone('America/Sao_Paulo')
#     df["tsIngestion"] = pd.to_datetime(datetime.now(tz))

#     df['planner_selectedDate'] = df['planner_selectedDate'].astype(str)
#     df['tsIngestion'] = df['tsIngestion'].astype(str)

#     return df

# @app.route('/planner', methods=['POST'])
# def planner():
#     try:
#         if request.headers.get('keyword') != PLANNER_PHRASE:
#             return jsonify({"message": "Unauthorized"}), 401

#         data = request.json.get('data')

#         if not data:
#             return jsonify({"message": "Cronograma não recebido."}), 400

#         flattened_data = {
#             "user_name": data["user"]["name"],
#             "user_email": data["user"]["email"],
#             "user_church": data["user"]["church"],
#             "planner_activities": data["planner"]["activities"],
#             "planner_selectedDate": data["planner"]["selectedDate"],
#             "planner_ministerSelected": data["planner"]["ministerSelected"],
#             "planner_worshipTitle": data["planner"]["worshipTitle"]
#         }

#         df = pd.DataFrame([flattened_data])
#         df = normalize_df(df)
#         insert_data(df)
#         return '', 201

#     except Exception as error:
#         return error_logging(error)

# # @app.route('/planner', methods=['GET'])
# # def get_planner():
# #     try:
# #         if request.headers.get('keyword') != PLANNER_PHRASE:
# #             return jsonify({"message": "Unauthorized"}), 401

# #         print(request)
# #         print(request.json)
# #         data = request.json.get('data')
# #         user_email = data.get('user_email')
# #         if not user_email:
# #             return jsonify({"message": "User email is required."}), 400

# #         creds = read_credentials()
# #         if not creds:
# #             raise Exception("Failed to load credentials.")

# #         client = bigquery.Client(credentials=creds, project=PROJECT_ID)
# #         query = f"""
# #             SELECT *
# #             FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}{TABLE_AMBIENT}`
# #             WHERE user_email = @user_email
# #             ORDER BY tsIngestion DESC
# #             LIMIT 1
# #         """
# #         job_config = bigquery.QueryJobConfig(
# #             query_parameters=[
# #                 bigquery.ScalarQueryParameter("user_email", "STRING", user_email)
# #             ]
# #         )
# #         query_job = client.query(query, job_config=job_config)
# #         results = query_job.result()

# #         rows = [dict(row) for row in results]
# #         if not rows:
# #             return jsonify({"message": "No data found for the given user email."}), 404

# #         flattened_data = {
# #             "activities": rows[0]["planner_activities"],
# #             "selectedDate": rows[0]["planner_selectedDate"],
# #             "ministerSelected": rows[0]["planner_ministerSelected"],
# #             "worshipTitle": rows[0]["planner_worshipTitle"],
# #         }

# #         return jsonify(flattened_data), 200

# #     except Exception as error:
# #         return error_logging(error)

if __name__ == '__main__':
    app.run(debug=True)
#     # from mock_data import post_planner, get_user_planner
#     # headers = {
#     #     "keyword": PLANNER_PHRASE
#     # }

#     # with app.test_request_context(
#     #     path="/planner",
#     #     method="GET",
#     #     headers=headers,
#     #     data=json.dumps(get_user_planner),
#     #     content_type="application/json",
#     # ):
#     #     response, status_code = get_planner()
#     #     print(f"Status Code: {status_code}")
#     #     if response != '':
#     #         print(f"Response: {response.get_json()}")
#     #     else:
#     #         print(f"Response: {response}")

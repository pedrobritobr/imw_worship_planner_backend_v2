from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import pytz
import pandas as pd
import json
from google.cloud import bigquery
from google.oauth2.service_account import Credentials

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from envs import PROJECT_ID, DATASET_ID, TABLE_ID, TABLE_AMBIENT, PLANNER_PHRASE, GCP_CREDS

app = Flask(__name__)
CORS(app)

def read_credentials():
    try:
        creds_dict = json.loads(GCP_CREDS)
        creds = Credentials.from_service_account_info(creds_dict)
        return creds
    except Exception as error:
        print(f"Error reading credentials: {error}")
        return None

def insert_data(df):
    creds = read_credentials()
    if not creds:
        raise Exception("Failed to load credentials.")

    table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}{TABLE_AMBIENT}"
    client = bigquery.Client(credentials=creds, project=PROJECT_ID)

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("user_name", "STRING"),
            bigquery.SchemaField("user_email", "STRING"),
            bigquery.SchemaField("user_church", "STRING"),
            bigquery.SchemaField("planner_activities", "RECORD", mode="REPEATED", fields=[
                bigquery.SchemaField("activityTitle", "STRING"),
                bigquery.SchemaField("duration", "INTEGER"),
                bigquery.SchemaField("hour", "STRING"),
                bigquery.SchemaField("id", "STRING"),
                bigquery.SchemaField("responsible", "STRING")
            ]),
            bigquery.SchemaField("planner_selectedDate", "DATE"),
            bigquery.SchemaField("planner_ministerSelected", "STRING"),
            bigquery.SchemaField("planner_worshipTitle", "STRING"),
            bigquery.SchemaField("tsIngestion", "TIMESTAMP")
        ],
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    )

    records = df.to_dict(orient='records')
    load_job = client.load_table_from_json(records, table_id, job_config=job_config)
    load_job.result()
    return

def error_logging(error):
    print(f"Error: {error}")
    return jsonify({"message": "Internal error."}), 500

def normalize_df(df):
    df["planner_selectedDate"] = pd.to_datetime(df["planner_selectedDate"]).dt.date
    df["planner_activities"] = df["planner_activities"].apply(
        lambda activities: [
            {**activity, "duration": int(activity["duration"])} for activity in activities
        ]
    )
 
    tz = pytz.timezone('America/Sao_Paulo')
    df["tsIngestion"] = pd.to_datetime(datetime.now(tz))

    df['planner_selectedDate'] = df['planner_selectedDate'].astype(str)
    df['tsIngestion'] = df['tsIngestion'].astype(str)

    return df

@app.route('/planner', methods=['POST'])
def planner():
    try:
        if request.headers.get('keyword') != PLANNER_PHRASE:
            return jsonify({"message": "Unauthorized"}), 401

        data = request.json.get('data')

        if not data:
            return jsonify({"message": "Cronograma não recebido."}), 400

        flattened_data = {
            "user_name": data["user"]["name"],
            "user_email": data["user"]["email"],
            "user_church": data["user"]["church"],
            "planner_activities": data["planner"]["activities"],
            "planner_selectedDate": data["planner"]["selectedDate"],
            "planner_ministerSelected": data["planner"]["ministerSelected"],
            "planner_worshipTitle": data["planner"]["worshipTitle"]
        }

        df = pd.DataFrame([flattened_data])
        df = normalize_df(df)
        insert_data(df)
        return '', 201

    except Exception as error:
        return error_logging(error)

@app.route('/')
def home():
    return 'about'

@app.route('/about')
def about():
    return f"{TABLE_ID}{TABLE_AMBIENT}"

if __name__ == '__main__':
    # app.run(debug=True)
    # from mock_data import mock_data
    # headers = {
    #     "keyword": PLANNER_PHRASE
    # }

    # with app.test_request_context(
    #     path="/planner",
    #     method="POST",
    #     headers=headers,
    #     data=json.dumps(mock_data),
    #     content_type="application/json",
    # ):
    #     response, status_code = planner()
    #     print(f"Status Code: {status_code}")
    #     if response != '':
    #         print(f"Response: {response.get_json()}")
    #     else:
    #         print(f"Response: {response}")

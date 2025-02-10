from google.cloud import bigquery
import pandas as pd

from flask import current_app

from app.service.schemas import planner_schema, user_schema

class UserNotFoundException(Exception):
    def __init__(self):
        super().__init__()

class PlannerNotFoundException(Exception):
    def __init__(self):
        super().__init__()

class BigQueryService:
    def __init__(self):
        config = current_app.config
        GCP_CREDS = config.get('GCP_CREDS')
        TABLE_AMBIENT = config.get('TABLE_AMBIENT')
        DATASET_ID = config.get('DATASET_ID')
        PROJECT_ID = config.get('PROJECT_ID')

        self.client = bigquery.Client(credentials=GCP_CREDS, project=PROJECT_ID)
        self.dataset_id = f"{PROJECT_ID}.{DATASET_ID}"
        self.table_ambient = TABLE_AMBIENT

        self.user_table = f"{self.dataset_id}.user_{self.table_ambient}"
        self.planner_table = f"{self.dataset_id}.planner_{self.table_ambient}"

    def record_table(self, records, schema, table) -> None:
        try:
            job_config = bigquery.LoadJobConfig(
                schema=schema,
                write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
                source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
            )

            load_job = self.client.load_table_from_json(records, table, job_config=job_config)
            load_job.result()

        except Exception as error:
            raise Exception(f"Failed to record table. {error}")

    def query_table(self, query, query_parameters):
        try:
            job_config = bigquery.QueryJobConfig(
                query_parameters=query_parameters
            )
            query_job = self.client.query(query, job_config=job_config)
            result = query_job.result()
            rows = [dict(row) for row in result]
            return pd.DataFrame(rows)
        except Exception as error:
            print(f"Error: {error}")
            raise Exception(f"Failed to query table. {error}")

    def record_planner(self, planner_df) -> None:
        records = planner_df.to_dict(orient='records')
        self.record_table(records, planner_schema, self.planner_table)

    def get_planner(self, email: str):
        try:
            query = f"""
                SELECT
                    * except(planner_activities),
                    TO_JSON(planner_activities) AS planner_activities
                FROM `{self.planner_table}`
                WHERE user_email = @email
                ORDER BY tsIngestion DESC
                LIMIT 1;
            """
            query_parameters=[bigquery.ScalarQueryParameter("email", "STRING", email)]
            result = self.query_table(query, query_parameters)
        except Exception as error:
            raise Exception(f"Erro ao recuperar último cronograma. Tente novamente mais tarde.")

        if result.empty:
            raise PlannerNotFoundException()

        return result.to_dict(orient='records')[0]


    def record_user(self, user) -> None:
        self.record_table(user, user_schema, self.user_table)

    def get_user(self, email: str):
        try:
            query = f"""
                SELECT *
                FROM `{self.user_table}`
                WHERE email = @email
                LIMIT 1
            """
            query_parameters=[bigquery.ScalarQueryParameter("email", "STRING", email)]
            result = self.query_table(query, query_parameters)

        except Exception as error:
            raise Exception(f"Erro ao recuperar usuário.")
        
        if result.empty:
            raise UserNotFoundException()
        return result.to_dict(orient='records')[0]

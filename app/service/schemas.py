from google.cloud import bigquery

planner_schema = [
    bigquery.SchemaField("planner_id", "STRING"),
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
    bigquery.SchemaField("planner_churchName", "STRING"),
    bigquery.SchemaField("tsIngestion", "TIMESTAMP")
]

user_schema = [
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("email", "STRING"),
    bigquery.SchemaField("church", "STRING"),
    bigquery.SchemaField("password", "STRING"),
    bigquery.SchemaField("tsIngestion", "TIMESTAMP")
]
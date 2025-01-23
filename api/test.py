# from google.cloud import bigquery
# from .schema import schema


# def create_inflow(
#     client: bigquery.Client,
#     PROJECT_ID,
#     DATASET_ID,
#     TABLE,
#     IMWCONTAB_ENV,
#     transaction_data,
# ):
#     write_disposition = bigquery.WriteDisposition.WRITE_APPEND
#     schema_update_options = [bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION]

#     job_config = bigquery.LoadJobConfig(
#         schema=schema,
#         write_disposition=write_disposition,
#         schema_update_options=schema_update_options,
#     )

#     result = client.load_table_from_dataframe(
#         dataframe=transaction_data,
#         job_config=job_config,
#         destination=f"{PROJECT_ID}.{DATASET_ID}.imw_{TABLE}_{IMWCONTAB_ENV}",
#     ).result()

#     output_rows = result.output_rows
#     return int(output_rows)
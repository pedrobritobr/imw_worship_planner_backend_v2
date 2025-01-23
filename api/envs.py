import os
from dotenv import load_dotenv

load_dotenv()

PLANNER_PHRASE = os.getenv('PLANNER_PHRASE')
GCP_CREDS = os.getenv('GCP_CREDS')
TABLE_AMBIENT = os.getenv('TABLE_AMBIENT')
DATASET_ID = os.getenv('DATASET_ID')
TABLE_ID = os.getenv('TABLE_ID')
PROJECT_ID = os.getenv('PROJECT_ID')

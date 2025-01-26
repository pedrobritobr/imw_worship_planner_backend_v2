import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    PLANNER_PHRASE = os.getenv('PLANNER_PHRASE')
    GCP_CREDS = os.getenv('GCP_CREDS')
    TABLE_AMBIENT = os.getenv('TABLE_AMBIENT')
    DATASET_ID = os.getenv('DATASET_ID')
    PROJECT_ID = os.getenv('PROJECT_ID')
    FERNET_KEY = os.getenv('FERNET_KEY')
    TOKEN_KEY = os.getenv('TOKEN_KEY')

    @staticmethod
    def validate():
        for key, value in Config.__dict__.items():
            if not key.startswith('__') and value is None:
                raise ValueError(f"Environment variable {key} is not set")

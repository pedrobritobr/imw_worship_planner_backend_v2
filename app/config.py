from google.oauth2.service_account import Credentials
import json

import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    def __init__(self):
        self.PLANNER_PHRASE = os.environ.get('PLANNER_PHRASE')
        self.GCP_CREDS = os.environ.get('GCP_CREDS')
        self.TABLE_AMBIENT = os.environ.get('TABLE_AMBIENT')
        self.DATASET_ID = os.environ.get('DATASET_ID')
        self.PROJECT_ID = os.environ.get('PROJECT_ID')
        self.FERNET_KEY = os.environ.get('FERNET_KEY')
        self.TOKEN_KEY = os.environ.get('TOKEN_KEY')

        self.validate()

        self.GCP_CREDS = self.get_credentials(self.GCP_CREDS)

    def get_credentials(self, GCP_CREDS):
        try:
            creds_dict = json.loads(GCP_CREDS)
            creds = Credentials.from_service_account_info(creds_dict)
            return creds
        except Exception as error:
            raise Exception(f"Error reading credentials {error}")

    def validate(self):
        for key, value in self.__dict__.items():
            if not key.startswith('__') and value is None:
                raise ValueError(f"Environment variable {key} is not set")

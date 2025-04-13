from flask import current_app
from google.cloud import storage

class CloudStorage:
    def __init__(self):
        config = current_app.config
        GCP_CREDS = config.get('GCP_CREDS')
        BUCKET_ID = config.get('DATASET_ID')
        PROJECT_ID = config.get('PROJECT_ID')

        self.client = storage.Client(credentials=GCP_CREDS, project=PROJECT_ID)
        self.bucket = self.client.bucket(BUCKET_ID)
        self.__create_bucket_is_not_exists()

        self.feedback_folder = f"feedback_{config.get('TABLE_AMBIENT')}"

    def __create_bucket_is_not_exists(self):
        try:
            if not self.bucket.exists():
                self.client.create_bucket(self.bucket)
        except Exception as error:
            raise Exception(f"Failed to create bucket. {error}")

    def upload_file(self, file, destination):
        blob = self.bucket.blob(destination)
        blob.upload_from_file(file, content_type=file.content_type)
        return f"gs://{self.bucket.name}/{destination}"

    def upload_feedback_files(self, files_data, folder_name):
        folder_name = f"{self.feedback_folder}/{folder_name}"
        
        image_urls = []
        errors = []
        for file in files_data.values():
            try:
                file_name = f"{folder_name}/{file.filename}"
                url = self.upload_file(file, file_name)

                image_urls.append(url)
            except Exception as e:
                error_json =  e.response.json()
                errors.append({
                    "file": file.filename,
                    "reason": error_json.get("error").get("message")
                })
        return (image_urls, errors)

    def delete_folder(self, folder_name):
        folder_name = f"{self.feedback_folder}/{folder_name}"

        blobs = self.client.list_blobs(self.bucket, prefix=folder_name)
        self.bucket.delete_blobs(list(blobs))

import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from werkzeug.utils import secure_filename

class GoogleDriveService:
    _instance = None  # Singleton instance
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GoogleDriveService, cls).__new__(cls)
            cls._instance._initialize_service()
        return cls._instance

    def _initialize_service(self):
        try:
            # Load credentials and initialize the Drive API service
            service_account_file_path = os.getenv("SERVICE_ACCOUNT_FILE")
            credentials = service_account.Credentials.from_service_account_file(
                service_account_file_path,
                scopes=['https://www.googleapis.com/auth/drive']
            )
            self.service = build('drive', 'v3', credentials=credentials)
        except Exception as e:
            print(f"Error initializing Google Drive service: {str(e)}")
            self.service = None

    def get_folder_id(self):
        return os.getenv("GOOGLE_DRIVE_FOLDER_ID")

    def upload_to_drive(self, file):
        # Secure filename and save temporarily
        filename = secure_filename(file.filename)
        # temp_filepath = os.path.join('uploads', filename)
        file.save(filename)

        try:
            if not self.service:
                raise Exception("Google Drive service is not initialized.")

            file_metadata = {
                'name': filename,
                'parents': [self.get_folder_id()]
            }
            media = MediaFileUpload(filename=filename, mimetype=file.content_type)
            
            # Upload file to Google Drive
            uploaded_file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            file_id = uploaded_file.get('id')

            # Set file permissions to public
            self.service.permissions().create(
                fileId=file_id,
                body={'role': 'reader', 'type': 'anyone'}
            ).execute()

            # Generate file URL
            file_url = f"https://drive.google.com/uc?id={file_id}"

            # Clean up temporary file
            os.remove(filename)

            return file_id, file_url

        except Exception as e:
            print(f"Error uploading file: {str(e)}")
            return None, None
        finally:
            # Ensure temp file is removed even if an error occurs
            if os.path.exists(filename):
                os.remove(filename)

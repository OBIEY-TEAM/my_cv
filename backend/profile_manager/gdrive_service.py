import os
import uuid
from django.conf import settings

class GoogleDriveService:
    @staticmethod
    def upload_pdf_file(uploaded_file, folder_name="candidatures"):
        """
        Uploads a PDF file to Google Drive and makes it publicly accessible.
        Fallback to returning local media server link if Google Drive service account
        is not configured in environment.
        """
        try:
            # Check for Google Drive API credentials
            credentials_path = getattr(settings, 'GOOGLE_DRIVE_CREDENTIALS_PATH', None) or os.getenv('GOOGLE_DRIVE_CREDENTIALS_PATH')
            if credentials_path and os.path.exists(credentials_path):
                from google.oauth2 import service_account
                from googleapiclient.discovery import build
                from googleapiclient.http import MediaFileUpload

                SCOPES = ['https://www.googleapis.com/auth/drive.file']
                creds = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
                drive_service = build('drive', 'v3', credentials=creds)

                file_metadata = {
                    'name': f"{uuid.uuid4().hex}_{uploaded_file.name}",
                    'mimeType': 'application/pdf'
                }

                # Save temporarily to disk for Google MediaFileUpload
                temp_path = os.path.join(settings.MEDIA_ROOT, 'temp', uploaded_file.name)
                os.makedirs(os.path.dirname(temp_path), exist_ok=True)
                with open(temp_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                media = MediaFileUpload(temp_path, mimetype='application/pdf')
                file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()

                # Make public
                permission = {'type': 'anyone', 'role': 'reader'}
                drive_service.permissions().create(fileId=file.get('id'), body=permission).execute()

                if os.path.exists(temp_path):
                    os.remove(temp_path)

                return file.get('webViewLink') or f"https://drive.google.com/file/d/{file.get('id')}/view"
        except Exception as e:
            print(f"Google Drive API Upload note: {e}")

        # Robust Fallback: Return absolute URL for locally stored media file
        if hasattr(uploaded_file, 'url'):
            return uploaded_file.url
        return ""

import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from shared.config import GOOGLE_APPLICATION_CREDENTIALS, DRIVE_DOWNLOAD_DIR

def download_google_drive_folder(folder_id: str, target_dir: str = DRIVE_DOWNLOAD_DIR, credentials_path: str = GOOGLE_APPLICATION_CREDENTIALS):
    """
    Downloads all files in a specific folder in Google Drive and returns their names.

    :param folder_id: Google Drive folder ID
    :param target_dir: Local directory to save files
    :param credentials_path: Path to the Service Account JSON file
    :return: List of downloaded file names
    """
    # Authentication
    creds = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=["https://www.googleapis.com/auth/drive"]
    )

    service = build('drive', 'v3', credentials=creds)

    os.makedirs(target_dir, exist_ok=True)

    print("🔍 Scanning folder...")
    query = f"'{folder_id}' in parents and trashed = false"
    response = service.files().list(q=query, fields="files(id, name)").execute()
    files = response.get("files", [])

    if not files:
        print("⚠️ No files found in the folder.")
        return []

    print(f"📁 {len(files)} files found. Downloading...")

    downloaded_files = []

    for file in files:
        file_id = file["id"]
        file_name = file["name"]
        file_path = os.path.join(target_dir, file_name)

        try:
            print(f"📥 Downloading: {file_name}")
            request = service.files().get_media(fileId=file_id)
            with io.FileIO(file_path, "wb") as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    _, done = downloader.next_chunk()
            downloaded_files.append(file_name)
        except Exception as e:
            print(f"❌ {file_name} could not be downloaded: {e}")

    print("✅ All files downloaded successfully.")
    return downloaded_files
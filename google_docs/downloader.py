import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from shared.config import GOOGLE_APPLICATION_CREDENTIALS

def fetch_google_docs_documents(credentials_path: str = GOOGLE_APPLICATION_CREDENTIALS):
    """
    Fetches a list of Google Docs documents.

    :param credentials_path: Path to the Service Account JSON file
    :return: List of document metadata
    """
    # Authentication
    creds = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=["https://www.googleapis.com/auth/documents.readonly"]
    )

    service = build('docs', 'v1', credentials=creds)

    print("🔍 Fetching Google Docs documents...")

    # Example: Fetch a specific document by ID (replace 'DOCUMENT_ID' with actual ID)
    document_id = "DOCUMENT_ID"  # Replace with actual document ID
    try:
        document = service.documents().get(documentId=document_id).execute()
        print(f"📄 Document fetched: {document.get('title', 'Unknown Document')}")
        return [document]
    except Exception as e:
        print(f"❌ Error fetching document: {e}")
        return []
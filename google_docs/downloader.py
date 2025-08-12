from typing import Optional, Dict, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from shared.config import SETTINGS, ensure_credentials


def fetch_document(
    document_id: str,
    credentials_path: Optional[str] = None,
    fields: str = "*"
) -> Optional[Dict[str, Any]]:
    """
    Tek bir Google Docs belgesini getirir.
    fields parametresi performans için kısıtlanabilir (örn: 'title,body/content')
    """
    cred_path = credentials_path or ensure_credentials(SETTINGS.default_credentials_filename)
    if not cred_path:
        raise FileNotFoundError("Credentials file not found.")

    creds = service_account.Credentials.from_service_account_file(
        cred_path, scopes=[SETTINGS.docs_api_scope]
    )
    service = build('docs', 'v1', credentials=creds)

    try:
        doc = service.documents().get(documentId=document_id).execute()
        return doc
    except HttpError as e:
        if e.resp.status == 404:
            print(f"[ERROR] Document {document_id} not found (404).")
        elif e.resp.status == 403:
            print(f"[ERROR] Permission denied for {document_id} (403).")
        else:
            print(f"[ERROR] HttpError while fetching {document_id}: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
    return None
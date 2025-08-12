from typing import Sequence, List
from shared.protocol import EmbeddingMethod
from googleapiclient.discovery import build
from google.oauth2 import service_account
import multiprocessing
import os
import json

class Document:
    """Simple document class"""
    def __init__(self, text, metadata=None):
        self.text = text
        self.metadata = metadata or {}

class BaseNode:
    """Simple node class"""
    def __init__(self, text, metadata=None):
        self.text = text
        self.metadata = metadata or {}

class GoogleDriveEmbeddingMethod(EmbeddingMethod):
    """Embedding method for Google Drive folders"""

    def __init__(self, folder_id: str, credentials_path: str = None):
        self.folder_id = folder_id
        self.credentials_path = credentials_path or "credentials.json"

    @staticmethod
    def customize_metadata(document: Document, data_source_id: str, **kwargs) -> Document:
        document.metadata = {
            "title": document.metadata.get("title", ""),
            "file_name": document.metadata.get("file_name", ""),
            "data_source": data_source_id,
            "source_type": "google_drive"
        }
        return document

    def apply_rules(
        self,
        documents: Sequence[Document],
        inclusion_rules: List[str],
        exclusion_rules: List[str],
    ) -> Sequence[Document]:
        # You can apply inclusion/exclusion rules here
        return documents

    def get_documents(self, data_source_id: str = "google_drive") -> Sequence[Document]:
        """Get documents from Google Drive folder"""
        try:
            # Set credentials path
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path
            print(f"[LOG] (Drive) Using credentials: {self.credentials_path}")
            
            # Read credentials.json as dict
            with open(self.credentials_path, 'r', encoding='utf-8') as f:
                service_account_dict = json.load(f)
            
            # Create credentials object
            creds = service_account.Credentials.from_service_account_info(
                service_account_dict, 
                scopes=["https://www.googleapis.com/auth/documents.readonly",
                       "https://www.googleapis.com/auth/drive.readonly"]
            )
            
            # Build Drive and Docs services
            drive_service = build('drive', 'v3', credentials=creds)
            docs_service = build('docs', 'v1', credentials=creds)
            
            print(f"[LOG] (Drive) Services created successfully.")
            
            # List files in the folder
            results = drive_service.files().list(
                q=f"'{self.folder_id}' in parents and mimeType='application/vnd.google-apps.document'",
                fields="files(id, name)"
            ).execute()
            
            files = results.get('files', [])
            documents = []
            
            print(f"[LOG] (Drive) Found {len(files)} documents in folder.")
            
            for file in files:
                try:
                    # Get document content
                    doc = docs_service.documents().get(documentId=file['id']).execute()
                    
                    # Extract text content
                    content_elements = doc.get("body", {}).get("content", [])
                    text_content = ""
                    
                    for element in content_elements:
                        if "paragraph" in element:
                            paragraph = element.get("paragraph", {})
                            elements = paragraph.get("elements", [])
                            for elem in elements:
                                text_run = elem.get("textRun", {})
                                content = text_run.get("content", "")
                                text_content += content
                    
                    # Create document
                    document = Document(
                        text=text_content,
                        metadata={
                            "title": file['name'],
                            "file_name": file['name'],
                            "file_id": file['id']
                        }
                    )
                    
                    # Customize metadata
                    self.customize_metadata(document, data_source_id)
                    documents.append(document)
                    
                except Exception as e:
                    print(f"[ERROR] Failed to process document {file['name']}: {e}")
            
            print(f"[LOG] (Docs) Documents loaded: {len(documents)}")
            return documents
            
        except Exception as e:
            print(f"Error loading documents from Google Drive: {e}")
            return []

    def download_and_process(self) -> Sequence[Document]:
        """Download and process documents from Google Drive"""
        return self.get_documents()

    def create_nodes(self, documents: Sequence[Document]) -> List[BaseNode]:
        """Create nodes from documents - simplified version"""
        nodes = []
        for doc in documents:
            # Split document into chunks (simplified)
            chunk_size = 1024
            text = doc.text
            
            for i in range(0, len(text), chunk_size):
                chunk = text[i:i + chunk_size]
                node = BaseNode(
                    text=chunk,
                    metadata=doc.metadata.copy()
                )
                nodes.append(node)
        
        return nodes

    def process(
        self,
        vector_store,
        task_manager,
        data_source_id: str,
        task_id: str,
        **kwargs,
    ) -> None:
        """Process documents - simplified implementation"""
        documents = self.get_documents(data_source_id)
        nodes = self.create_nodes(documents)
        return nodes
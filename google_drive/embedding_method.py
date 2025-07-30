from typing import Sequence, List
from shared.protocol import EmbeddingMethod
from llama_index.core.schema import Document, BaseNode
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.google import GoogleDriveReader
from llama_index.core import SimpleDirectoryReader
import multiprocessing
import os

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
            import json
            with open(self.credentials_path, 'r', encoding='utf-8') as f:
                service_account_dict = json.load(f)
            # Explicitly pass service_account_key as dict to GoogleDriveReader
            reader = GoogleDriveReader(service_account_key=service_account_dict)
            print(f"[LOG] (Drive) Reader created with service_account_key.")
            # Load documents from Google Drive
            documents = reader.load_data(folder_id=self.folder_id)
            print(f"[LOG] (Drive) Documents loaded: {len(documents) if documents else 0}")
            # Customize metadata for each document
            for doc in documents:
                self.customize_metadata(doc, data_source_id)
            return documents
        except Exception as e:
            print(f"Error loading documents from Google Drive: {e}")
            return []

    def download_and_process(self) -> Sequence[Document]:
        """Download and process documents from Google Drive"""
        return self.get_documents()

    def create_nodes(self, documents: Sequence[Document]) -> List[BaseNode]:
        """Create nodes from documents"""
        # Create ingestion pipeline
        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(chunk_size=1024, chunk_overlap=20)
            ]
        )
        
        # Process documents through pipeline
        nodes = pipeline.run(documents=documents)
        return nodes

    def process(
        self,
        vector_store,
        task_manager,
        data_source_id: str,
        task_id: str,
        **kwargs,
    ) -> None:
        pass 
import os
import json
from typing import Sequence, List
from shared.protocol import EmbeddingMethod
from llama_index.core.schema import Document, BaseNode
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.google import GoogleDocsReader

from shared.config import SETTINGS, ensure_credentials


class GoogleDriveEmbeddingMethod(EmbeddingMethod):
    """
    Belirli bir Google Drive klasöründeki Google Docs belgelerini okuyup
    node'lara parçalayan embedding yöntemi.
    """

    def __init__(self, folder_id: str, credentials_path: str = None):
        self.folder_id = folder_id
        self.credentials_path = credentials_path

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
        # Basit inclusion/exclusion örneği (title bazlı)
        if not inclusion_rules and not exclusion_rules:
            return documents

        def included(doc: Document) -> bool:
            title_lower = (doc.metadata.get("title") or "").lower()
            if inclusion_rules and not any(r.lower() in title_lower for r in inclusion_rules):
                return False
            if exclusion_rules and any(r.lower() in title_lower for r in exclusion_rules):
                return False
            return True

        return [d for d in documents if included(d)]

    def _load_reader(self) -> GoogleDocsReader:
        cred_path = self.credentials_path or ensure_credentials(SETTINGS.default_credentials_filename)
        if not cred_path:
            raise FileNotFoundError("Google credentials not found. Provide a valid credentials path.")
        with open(cred_path, "r", encoding="utf-8") as f:
            service_account_dict = json.load(f)
        reader = GoogleDocsReader(service_account_key=service_account_dict)
        return reader

    def get_documents(self, data_source_id: str = "google_drive") -> Sequence[Document]:
        try:
            reader = self._load_reader()
            documents = reader.load_data(folder_id=self.folder_id)
            for doc in documents:
                self.customize_metadata(doc, data_source_id)
            return documents
        except Exception as e:
            print(f"[ERROR] Loading documents failed: {e}")
            return []

    def download_and_process(self, **kwargs) -> Sequence[Document]:
        return self.get_documents(**kwargs)

    def create_nodes(self, documents: Sequence[Document]) -> List[BaseNode]:
        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(
                    chunk_size=SETTINGS.chunk_size,
                    chunk_overlap=SETTINGS.chunk_overlap
                )
            ]
        )
        nodes = pipeline.run(documents=list(documents))
        return nodes

    def process(
        self,
        vector_store,
        task_manager,
        data_source_id: str,
        task_id: str,
        inclusion_rules=None,
        exclusion_rules=None,
        **kwargs,
    ) -> None:
        """
        Örnek process akışı:
          1. Belgeleri al
          2. Kuralları uygula
          3. Node oluştur
          4. vector_store'a yaz (ör: add_nodes)
        """
        documents = self.get_documents(data_source_id=data_source_id)
        filtered = self.apply_rules(documents, inclusion_rules or [], exclusion_rules or [])
        if not filtered:
            print(f"[INFO] No documents after filtering in task {task_id}.")
            return
        nodes = self.create_nodes(filtered)

        # vector_store arayüzü soyut; örnek: vector_store.add(nodes)
        # Projene göre uyarlaman gerekir.
        if hasattr(vector_store, "add"):
            vector_store.add(nodes)
        elif hasattr(vector_store, "add_nodes"):
            vector_store.add_nodes(nodes)
        else:
            print("[WARN] Vector store does not support add/add_nodes interface.")

        # task_manager ileride progress için kullanılabilir
        if task_manager and hasattr(task_manager, "notify"):
            task_manager.notify(task_id, f"Processed {len(nodes)} nodes")
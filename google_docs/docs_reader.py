import os
import json
import tempfile
import shutil
from contextlib import contextmanager
from typing import Dict, Any, List, Sequence

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

from llama_index.core import Document
from llama_index.core.schema import BaseNode
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter

from shared.config import SETTINGS


class InvalidDataSourceConfigException(Exception):
    """Hatalı veya eksik konfigürasyon durumunda fırlatılır."""


REQUIRED_SERVICE_ACCOUNT_KEYS = [
    "type",
    "project_id",
    "private_key_id",
    "private_key",
    "client_email",
    "client_id",
    "auth_uri",
    "token_uri",
    "auth_provider_x509_cert_url",
    "client_x509_cert_url",
    "universe_domain",
]


@contextmanager
def credentials_context(config: Dict[str, Any]):
    """Geçici çalışma klasörü oluşturarak config'i token.json'a kaydeder.

    Adımlar:
      1. Mevcut dizini kaydet
      2. mkdtemp ile temp klasör oluştur
      3. temp klasöre chdir
      4. config tamamını token.json'a yaz
      5. yield sonrası eski dizine dön ve temp'i sil
    """
    prev_cwd = os.getcwd()
    temp_dir = tempfile.mkdtemp(prefix="gdocs_cfg_")
    try:
        os.chdir(temp_dir)
        with open("token.json", "w", encoding="utf-8") as f:
            json.dump(config, f)
        yield
    finally:
        os.chdir(prev_cwd)
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass


def _extract_text_from_doc(raw_doc: Dict[str, Any]) -> str:
    body = raw_doc.get("body", {})
    contents = body.get("content", [])
    acc: List[str] = []
    for el in contents:
        para = el.get("paragraph")
        if not para:
            continue
        for elem in para.get("elements", []):
            text_run = elem.get("textRun")
            if not text_run:
                continue
            content = text_run.get("content", "")
            if content:
                acc.append(content)
    return "".join(acc).strip()


class GoogleDocsConfigReader:
    """Config tabanlı, bir veya birden çok Google Docs belgesini indeksleyen sınıf.

    Beklenen config anahtarları:
      - service_account_dict: Service account JSON dict
      - document_ids: List[str]
      - inclusion_rules: List[str] (opsiyonel boş liste olabilir)
      - exclusion_rules: List[str]
    """

    REQUIRED_KEYS = [
        "service_account_dict",
        "document_ids",
        "inclusion_rules",
        "exclusion_rules",
    ]

    def __init__(self, data_source_id: str, config: Dict[str, Any]):
        self.data_source_id = data_source_id
        self.config = config
        self.validate_config(config)

    def validate_config(self, config: Dict[str, Any]):
        for k in self.REQUIRED_KEYS:
            if k not in config:
                raise InvalidDataSourceConfigException(
                    f"GoogleDocsConfigReader requires '{k}' in config."
                )
        sa = config["service_account_dict"]
        for k in REQUIRED_SERVICE_ACCOUNT_KEYS:
            if k not in sa:
                raise InvalidDataSourceConfigException(
                    f"GoogleDocsConfigReader requires '{k}' in 'service_account_dict'."
                )
        if not isinstance(config.get("document_ids"), list) or not config["document_ids"]:
            raise InvalidDataSourceConfigException("'document_ids' must be a non-empty list")

    def _build_service(self):
        creds = service_account.Credentials.from_service_account_info(
            self.config["service_account_dict"], scopes=[SETTINGS.docs_api_scope]
        )
        return build("docs", "v1", credentials=creds)

    def get_documents(self, *args, **kwargs) -> Sequence[Document]:
        docs: List[Document] = []
        inclusion = [r.lower() for r in self.config.get("inclusion_rules", [])]
        exclusion = [r.lower() for r in self.config.get("exclusion_rules", [])]
        with credentials_context(self.config):
            service = self._build_service()
            for doc_id in self.config["document_ids"]:
                try:
                    raw = service.documents().get(documentId=doc_id).execute()
                except HttpError as e:
                    print(f"[ERROR] {doc_id} fetch failed: {e}")
                    continue
                title = raw.get("title", "")
                tl = title.lower()
                if inclusion and not any(r in tl for r in inclusion):
                    continue
                if exclusion and any(r in tl for r in exclusion):
                    continue
                text = _extract_text_from_doc(raw)
                if not text:
                    continue
                docs.append(
                    Document(
                        text=text,
                        metadata={
                            "title": title,
                            "doc_id": doc_id,
                            "data_source": self.data_source_id,
                            "source_type": "google_docs",
                        },
                    )
                )
        return docs

    def create_nodes(self, documents: Sequence[Document]) -> List[BaseNode]:
        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(
                    chunk_size=SETTINGS.chunk_size,
                    chunk_overlap=SETTINGS.chunk_overlap,
                )
            ]
        )
        return pipeline.run(documents=list(documents))

    def process(
        self,
        vector_store,
        task_manager,
        data_source_id: str,
        task_id: str,
        **kwargs,
    ) -> None:
        documents = self.get_documents()
        if not documents:
            print(f"[INFO] No documents processed for task {task_id}.")
            return
        nodes = self.create_nodes(documents)
        if hasattr(vector_store, "add"):
            vector_store.add(nodes)
        elif hasattr(vector_store, "add_nodes"):
            vector_store.add_nodes(nodes)
        else:
            print("[WARN] Vector store does not support add/add_nodes interface.")
        if task_manager and hasattr(task_manager, "notify"):
            task_manager.notify(task_id, f"Processed {len(nodes)} nodes")

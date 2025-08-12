from typing import Sequence
import os
from llama_index.core import Document, VectorStoreIndex, StorageContext, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Bu modülde OpenAI yerine HuggingFace embedding modeli ZORUNLU olarak kuruluyor.
# Böylece OPENAI_API_KEY bulunamadı hatası alınmaz.

_EMBED_MODEL = None  # lazy init


def setup_llama_index():
    """HuggingFace embedding modelini global Settings'e uygular.

    Ortam değişkeni: HUGGINGFACE_EMBED_MODEL
      Belirtilmezse varsayılan: sentence-transformers/all-MiniLM-L6-v2
    """
    global _EMBED_MODEL
    if _EMBED_MODEL is not None:
        return

    model_name = os.environ.get("HUGGINGFACE_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    try:
        _EMBED_MODEL = HuggingFaceEmbedding(model_name=model_name)
        Settings.embed_model = _EMBED_MODEL
        # Eğer daha sonra LLM eklemek istersen (ör: local), Settings.llm = ... ekleyebilirsin.
    except Exception as e:
        # Kullanıcıya kısa bilgi bırakıyoruz; indeks oluşturma çağrıları bu embed_model olmadan çalışmayacak.
        raise RuntimeError(f"HuggingFace embedding modeli yüklenemedi: {model_name} -> {e}")


def build_nodes_from_documents(
    documents: Sequence[Document],
    chunk_size: int = 1024,
    chunk_overlap: int = 20
):
    splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    nodes = splitter.get_nodes_from_documents(list(documents))
    return nodes


def create_index_from_documents(
    documents: Sequence[Document],
    chunk_size: int = 1024,
    chunk_overlap: int = 20
):
    """
    Gerçek bir VectorStoreIndex oluşturur. Dönen obje sorgulanabilir.
    """
    nodes = build_nodes_from_documents(documents, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    storage_context = StorageContext.from_defaults()
    index = VectorStoreIndex(nodes, storage_context=storage_context)
    return index
from llama_index.core import VectorStoreIndex, Document, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.gemini import Gemini
from llama_index.core.settings import Settings
from shared.config import EMBEDDING_MODEL, LLM_MODEL, INDEX_STORAGE_DIR, GOOGLE_API_KEY
import os

def setup_llama_index():
    """Setup LlamaIndex with HuggingFace embedding and Gemini LLM"""
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL, device='cpu')
    
    # Configure Gemini with API key if available
    if GOOGLE_API_KEY:
        Settings.llm = Gemini(model=LLM_MODEL, api_key=GOOGLE_API_KEY)
    else:
        # Try to use default credentials
        try:
            Settings.llm = Gemini(model=LLM_MODEL)
        except Exception as e:
            print(f"Warning: Could not initialize Gemini LLM: {e}")
            print("Please set GOOGLE_API_KEY environment variable or upload credentials")
            # Use a fallback or raise an error
            raise Exception("Google API Key is required for Gemini LLM. Please set GOOGLE_API_KEY environment variable.")

def create_index_from_documents(documents, persist_dir=None):
    """Create index from documents"""
    if persist_dir is None:
        persist_dir = INDEX_STORAGE_DIR
    
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=persist_dir)
    return index

def load_existing_index(persist_dir=None):
    """Load existing index from storage"""
    if persist_dir is None:
        persist_dir = INDEX_STORAGE_DIR
    
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    index = load_index_from_storage(storage_context)
    return index

def create_query_engine(index):
    """Create query engine from index"""
    return index.as_query_engine()

def ask_question(query_engine, question: str):
    """Ask a question using the query engine"""
    return query_engine.query(question) 
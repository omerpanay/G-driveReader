import os

# API Keys - Use environment variables for security
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")

# Google Drive Settings
# Make sure this folder ID is correct and accessible
DRIVE_FOLDER_ID = "1zyKR8R9SxhOmp4wCqTlojNb9SZMZJfkF"
DRIVE_DOWNLOAD_DIR = "./drive_downloads"

# Google Docs Settings
DOCS_DOCUMENT_ID = "1sJjoOHvUMwFX7q0iU8aUnOS4d6889QDT_YTernsJgAk"

# LlamaIndex Settings
INDEX_STORAGE_DIR = "llama_index_storage"
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash")

# Environment setup
def setup_environment():
    """Setup environment variables for Google APIs"""
    # GOOGLE_API_KEY is already set from main.py if provided
    # GOOGLE_APPLICATION_CREDENTIALS is set from uploaded file
    pass

def get_credentials_path():
    """Get the current credentials path"""
    return os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json") 
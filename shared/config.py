import os
from dataclasses import dataclass
from typing import Optional

# Basit bir yapılandırma objesi. İleride pydantic BaseSettings'e taşınabilir.
@dataclass
class AppSettings:
    credentials_env_var: str = "GOOGLE_APPLICATION_CREDENTIALS"
    default_credentials_filename: str = "credentials.json"
    docs_api_scope: str = "https://www.googleapis.com/auth/documents.readonly"
    # İleride Drive API eklemek istersen:
    drive_api_scope: str = "https://www.googleapis.com/auth/drive.readonly"
    
    chunk_size: int = 1024
    chunk_overlap: int = 20

SETTINGS = AppSettings()


def set_credentials_path(path: str) -> None:
    """
    Güvenli şekilde environment değişkenini günceller.
    """
    if not path:
        return
    os.environ[SETTINGS.credentials_env_var] = path


def get_credentials_path() -> Optional[str]:
    return os.environ.get(SETTINGS.credentials_env_var)


def ensure_credentials(fallback: str = None) -> Optional[str]:
    """
    Eğer env'de yoksa fallback'i (örn. credentials.json) kullanır.
    """
    current = get_credentials_path()
    if current and os.path.exists(current):
        return current
    if fallback and os.path.exists(fallback):
        set_credentials_path(fallback)
        return fallback
    return None
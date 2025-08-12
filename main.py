import streamlit as st
import os
import json
import secrets
import tempfile
from pathlib import Path
from google_docs.chat_interface import run_documents_chat
from shared.config import set_credentials_path, SETTINGS


def save_credentials_securely(raw_content: str) -> str:
    """
    Kullanıcıdan gelen JSON içeriğini doğrular ve benzersiz bir temp dosyaya yazar.
    """
    parsed = json.loads(raw_content)  # JSON doğrulama
    if "client_email" not in parsed:
        raise ValueError("Geçersiz credentials (client_email yok).")

    tmp_dir = Path(tempfile.gettempdir())
    file_name = f"gcred_{secrets.token_hex(8)}.json"
    cred_path = tmp_dir / file_name
    cred_path.write_text(json.dumps(parsed), encoding="utf-8")

    try:
        os.chmod(cred_path, 0o600)
    except Exception:
        pass  # Windows vb. ortamda sorun olabilir

    set_credentials_path(str(cred_path))
    st.session_state["credentials_path"] = str(cred_path)
    return str(cred_path)


def handle_credentials_input():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔐 Google API Credentials")

    existing = st.session_state.get("credentials_path")
    if existing and Path(existing).exists():
        st.sidebar.success("✅ Credentials yüklü.")
        return True

    content = st.sidebar.text_area(
        "credentials.json içeriğini yapıştır",
        help="Google Service Account JSON dosyanızın içeriği",
        height=220
    )

    if content.strip():
        try:
            path = save_credentials_securely(content.strip())
            st.sidebar.success(f"✅ Kaydedildi: {path}")
            return True
        except json.JSONDecodeError as e:
            st.sidebar.error(f"JSON parse hatası: {e}")
        except Exception as e:
            st.sidebar.error(f"Kaydetme hatası: {e}")
    return False


def cleanup_credentials():
    cred_path = st.session_state.get("credentials_path")
    if cred_path and os.path.exists(cred_path):
        try:
            os.unlink(cred_path)
        except Exception as e:
            st.sidebar.warning(f"Silinemedi: {e}")
    st.session_state.pop("credentials_path", None)
    os.environ.pop(SETTINGS.credentials_env_var, None)


def render_help():
    st.info(
        """
        Nasıl alınır:
        1. Google Cloud Console
        2. Proje seç / oluştur
        3. Docs API etkinleştir
        4. Service Account oluştur
        5. JSON anahtar indir
        6. İçeriği buraya yapıştır
        """
    )


def main():
    st.set_page_config(page_title="Google Docs Reader", page_icon="📄", layout="wide")
    st.title("📄 Google Docs File Reader")

    if not handle_credentials_input():
        st.warning("Önce credentials gir.")
        render_help()
        return

    document_id = st.text_input(
        "Google Document ID",
        help="Belge URL'sinde /d/ ile /edit arasındaki kısım."
    )

    if st.button("📄 Oku"):
        if not document_id.strip():
            st.error("Document ID gerekli.")
        else:
            run_documents_chat(document_id.strip())

    if st.sidebar.button("🗑️ Credentials Temizle"):
        cleanup_credentials()
        st.rerun()


if __name__ == "__main__":
    main()
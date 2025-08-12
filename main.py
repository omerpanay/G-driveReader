import streamlit as st
import os
import json
import secrets
import tempfile
from pathlib import Path
from google_docs.chat_interface import run_documents_chat
from google_docs.docs_reader import GoogleDocsConfigReader
from shared.llama_utils import setup_llama_index, create_index_from_documents
from shared.config import set_credentials_path, SETTINGS


def save_credentials_securely(raw_content: str) -> str:
    """Validate raw JSON key content and store in a unique temp file."""
    parsed = json.loads(raw_content)  # JSON validation
    if "client_email" not in parsed:
        raise ValueError("Invalid credentials (missing client_email).")

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
        st.sidebar.success("✅ Credentials loaded.")
        return True

    content = st.sidebar.text_area(
        "Paste credentials.json content",
        help="Full content of your Google Service Account JSON key",
        height=220
    )

    if content.strip():
        try:
            path = save_credentials_securely(content.strip())
            st.sidebar.success(f"✅ Saved: {path}")
            return True
        except json.JSONDecodeError as e:
            st.sidebar.error(f"JSON parse error: {e}")
        except Exception as e:
            st.sidebar.error(f"Save error: {e}")
    return False


def cleanup_credentials():
    cred_path = st.session_state.get("credentials_path")
    if cred_path and os.path.exists(cred_path):
        try:
            os.unlink(cred_path)
        except Exception as e:
            st.sidebar.warning(f"Could not delete: {e}")
    st.session_state.pop("credentials_path", None)
    os.environ.pop(SETTINGS.credentials_env_var, None)


def render_help():
    st.info(
        """
        How to obtain credentials:
        1. Open Google Cloud Console
        2. Select / create a project
        3. Enable the Google Docs API
        4. Create a Service Account
        5. Generate a JSON key
        6. Paste its content here
        """
    )


def main():
    st.set_page_config(page_title="Google Docs Reader", page_icon="📄", layout="wide")
    st.title("📄 Google Docs File Reader")

    if not handle_credentials_input():
        st.warning("Enter credentials first.")
        render_help()
        return

    tab_single, tab_multi = st.tabs(["Single Document", "Multiple Documents"])

    with tab_single:
        document_id = st.text_input(
            "Google Document ID",
            help="The part between /d/ and /edit in the document URL."
        )
        if st.button("📄 Load"):
            if not document_id.strip():
                st.error("Document ID required.")
            else:
                run_documents_chat(document_id.strip())

    with tab_multi:
        st.subheader("Index Multiple Google Docs")
        multi_ids_raw = st.text_area(
            "Document IDs (one per line)",
            help="Only the ID part (between /d/ and /edit) for each document."
        )
        inclusion_raw = st.text_area("Inclusion Rules (optional)", help="Words that must appear in the title")
        exclusion_raw = st.text_area("Exclusion Rules (optional)", help="Words that exclude a doc if present in the title")
        if st.button("📚 Index Documents"):
            doc_ids = [l.strip() for l in multi_ids_raw.splitlines() if l.strip()]
            if not doc_ids:
                st.error("Enter at least one Document ID.")
            else:
                cred_path = st.session_state.get("credentials_path")
                try:
                    with open(cred_path, "r", encoding="utf-8") as f:
                        service_account_dict = json.load(f)
                except Exception as e:
                    st.error(f"Could not read credentials: {e}")
                    service_account_dict = None
                if service_account_dict:
                    config = {
                        "service_account_dict": service_account_dict,
                        "document_ids": doc_ids,
                        "inclusion_rules": [l.strip() for l in inclusion_raw.splitlines() if l.strip()],
                        "exclusion_rules": [l.strip() for l in exclusion_raw.splitlines() if l.strip()],
                    }
                    try:
                        reader = GoogleDocsConfigReader(data_source_id="google_docs", config=config)
                        setup_llama_index()
                        documents = reader.get_documents()
                        if not documents:
                            st.warning("No documents passed the filters or contents are empty.")
                        else:
                            index = create_index_from_documents(documents, chunk_size=SETTINGS.chunk_size, chunk_overlap=SETTINGS.chunk_overlap)
                            st.success(f"{len(documents)} documents indexed.")
                            st.write("Sample Titles:")
                            for d in documents[:10]:
                                st.write(f"- {d.metadata.get('title','(no title)')}")
                            # İleride sorgulama için session'da sakla
                            st.session_state["multi_docs_index"] = index
                            st.info("Index stored in session_state['multi_docs_index'] (you can add a query UI).")
                    except Exception as e:
                        st.error(f"Indexing error: {e}")

    if st.sidebar.button("🗑️ Clear Credentials"):
        cleanup_credentials()
        st.rerun()


if __name__ == "__main__":
    main()
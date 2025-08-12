import streamlit as st
from googleapiclient.errors import HttpError
from llama_index.core import Document

from shared.llama_utils import setup_llama_index, create_index_from_documents
from shared.config import SETTINGS, ensure_credentials
from google_docs.downloader import fetch_document


def extract_text_from_doc(document: dict) -> str:
    """
    Google Docs API dönen 'body.content' yapısından tüm textRun içeriklerini çıkarır.
    Önceki sürüm yalnızca ilk element'i alıyordu—bu daha eksiksiz.
    """
    body = document.get("body", {})
    contents = body.get("content", [])
    texts = []
    for element in contents:
        para = element.get("paragraph")
        if not para:
            continue
        for elem in para.get("elements", []):
            text_run = elem.get("textRun")
            if not text_run:
                continue
            content = text_run.get("content", "")
            if content:
                texts.append(content)
    return "".join(texts).strip()


def build_index_from_document(document_id: str):
    """
    UI'dan bağımsız iş mantığı: belgeyi getir → text çıkar → Document → index oluştur → döndür.
    """
    ensure_credentials()  # Gerekirse env'i hazırlar
    raw_doc = fetch_document(document_id=document_id)
    if not raw_doc:
        raise ValueError(f"Document not found or inaccessible: {document_id}")

    text_content = extract_text_from_doc(raw_doc)
    if not text_content:
        raise ValueError("Belge içeriği boş veya çözümlenemedi.")

    formatted = Document(
        text=text_content,
        metadata={"title": raw_doc.get("title", "Unknown Document"), "doc_id": document_id}
    )

    setup_llama_index()
    index = create_index_from_documents([formatted], chunk_size=SETTINGS.chunk_size, chunk_overlap=SETTINGS.chunk_overlap)
    return index, formatted


def run_documents_chat(document_id: str):
    """
    Orijinal fonksiyonun geliştirilmiş hali.
    Streamlit'e yazım burada kalıyor ancak iş mantığı build_index_from_document içinde.
    """
    st.write("📄 Belge okunuyor...")

    try:
        index, formatted = build_index_from_document(document_id)
        st.success("Belge başarıyla okundu & indeks oluşturuldu.")
        st.write("### Başlık:")
        st.write(f"- {formatted.metadata.get('title')}")
        st.write("### İçerik (kırpılmış olabilir):")
        preview = formatted.text[:4000] + ("... (truncated)" if len(formatted.text) > 4000 else "")
        st.code(preview, language="text")
        return {
            "title": formatted.metadata.get("title"),
            "length": len(formatted.text),
            "index": index,
        }
    except HttpError as e:
        st.error(f"API hatası: {e}")
    except Exception as e:
        st.error(f"Hata: {e}")
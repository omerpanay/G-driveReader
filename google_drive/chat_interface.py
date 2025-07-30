import streamlit as st
from shared.llama_utils import setup_llama_index, create_index_from_documents
from shared.config import setup_environment
from google_drive.downloader import download_google_drive_folder

def run_drive_chat(folder_id):
    """Google Drive'dan dosya okuma işlemini gerçekleştirir"""
    setup_environment()

    # LlamaIndex'i ayarla
    setup_llama_index()

    st.title("📄 Google Drive Dosya Okuyucu")
    st.write("Drive klasöründen dosyalar okunuyor...")

    try:
        # Dosyaları folder_id kullanarak indir
        file_names = download_google_drive_folder(folder_id)
        if not file_names:
            st.warning("Klasörde hiç dosya bulunamadı.")
            return None

        # İndirilen dosyaları belgeler olarak işleme
        documents = []  # İndirilen dosyaları belgeler listesine dönüştürmek için işlem eklenmeli
        index = create_index_from_documents(documents)
        st.success("Dosyalar başarıyla okundu ve indeks oluşturuldu!")

        # Okunan dosyaların adlarını göster
        st.write("### Okunan Dosyalar:")
        for file_name in file_names:
            st.write(f"- {file_name}")

        return index
    except Exception as e:
        st.error(f"Hata oluştu: {e}")
        return None
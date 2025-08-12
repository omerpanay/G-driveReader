import streamlit as st
import os
import json
import re
from google_docs.chat_interface import run_documents_chat

def validate_credentials_json(credentials_content):
    """Validate that the credentials content is valid JSON with required fields"""
    try:
        creds = json.loads(credentials_content)
        required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
        
        for field in required_fields:
            if field not in creds:
                return False, f"Missing required field: {field}"
        
        if creds.get('type') != 'service_account':
            return False, "Credentials must be for a service account"
            
        return True, "Valid credentials"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON format: {e}"
    except Exception as e:
        return False, f"Error validating credentials: {e}"

def validate_document_id(document_id):
    """Validate Google Document ID format"""
    if not document_id:
        return False, "Document ID cannot be empty"
    
    # Basic validation - Google Doc IDs are typically 44 characters long and alphanumeric with some special chars
    if len(document_id) < 20:
        return False, "Document ID appears to be too short"
    
    # Check for valid characters (letters, numbers, hyphens, underscores)
    if not re.match(r'^[a-zA-Z0-9_-]+$', document_id):
        return False, "Document ID contains invalid characters"
    
    return True, "Valid document ID"

def handle_credentials_input():
    """Accepts credentials.json content from the user"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔐 Google API Credentials")
    credentials_content = st.sidebar.text_area(
        "Paste your credentials.json content",
        help="Paste the content of your Google Service Account credentials file",
        height=150
    )
    
    if credentials_content:
        # Validate credentials format
        is_valid, message = validate_credentials_json(credentials_content)
        
        if not is_valid:
            st.sidebar.error(f"❌ Invalid credentials: {message}")
            return False
        
        try:
            credentials_path = os.path.abspath('credentials.json')
            with open(credentials_path, 'w', encoding='utf-8') as f:
                f.write(credentials_content)
            st.session_state['credentials_path'] = credentials_path
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
            st.sidebar.success("✅ Credentials saved successfully!")
            return True
        except Exception as e:
            st.sidebar.error(f"❌ Error saving credentials: {e}")
            return False
    
    if 'credentials_path' in st.session_state and os.path.exists(st.session_state['credentials_path']):
        st.sidebar.success("✅ Credentials already saved")
        return True
    
    return False

def cleanup_credentials():
    """Deletes the uploaded credentials file"""
    if 'credentials_path' in st.session_state:
        try:
            if os.path.exists(st.session_state['credentials_path']):
                os.unlink(st.session_state['credentials_path'])
            del st.session_state['credentials_path']
            if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
                del os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        except Exception as e:
            st.sidebar.error(f"Error cleaning up credentials: {e}")

def main():
    st.set_page_config(
        page_title="Google Docs File Reader",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 Google Docs File Reader")
    st.write("Bu uygulama Google Docs'tan belgeleri okumak ve içeriklerini görüntülemek için tasarlanmıştır.")
    
    # Instructions section
    with st.expander("📖 Nasıl Kullanılır", expanded=False):
        st.markdown("""
        **Adım 1: Google Cloud Console'da kurulum yapın**
        1. [Google Cloud Console](https://console.cloud.google.com/)'a gidin
        2. Yeni bir proje oluşturun veya mevcut bir projeyi seçin
        3. Google Docs API'sini etkinleştirin
        4. Bir Service Account oluşturun
        5. JSON key dosyasını indirin
        
        **Adım 2: Credentials'ı yükleyin**
        1. Sol panelden JSON key dosyasının içeriğini kopyalayıp yapıştırın
        
        **Adım 3: Belgeyi okuyun**
        1. Google Docs belgenizin ID'sini girin
        2. "📄 Belgeyi Oku" butonuna tıklayın
        
        **Google Docs ID'si nasıl bulunur:**
        - Google Docs URL'sinde `/d/` ve `/edit` arasındaki kısım ID'dir
        - Örnek: `https://docs.google.com/document/d/[DOCUMENT_ID]/edit`
        """)

    credentials_saved = handle_credentials_input()
    
    if not credentials_saved:
        st.warning("⚠️ Lütfen Google API credentials.json içeriğini girin.")
        return

    st.markdown("---")
    
    # Document ID input with validation
    document_id = st.text_input(
        "📄 Google Document ID", 
        help="Belgenin URL'sinden document ID'sini kopyalayın",
        placeholder="Örnek: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
    )
    
    if document_id:
        is_valid, message = validate_document_id(document_id)
        if not is_valid:
            st.error(f"❌ {message}")
            return
        else:
            st.success(f"✅ {message}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("📄 Belgeyi Oku", type="primary", disabled=not document_id):
            if not document_id:
                st.error("Lütfen bir Document ID girin!")
            else:
                with st.spinner("Belge okunuyor..."):
                    try:
                        # Call run_documents_chat with the Document ID
                        result = run_documents_chat(document_id=document_id)
                        if result and not result.startswith("API error") and not result.startswith("An error"):
                            st.success("✅ Belge başarıyla okundu!")
                        else:
                            st.error("❌ Belge okunamadı. Hata detayları yukarıda gösterildi.")
                    except Exception as e:
                        st.error(f"❌ Beklenmeyen bir hata oluştu: {e}")
    
    with col2:
        if st.button("🗑️ Credentials'ı Temizle"):
            cleanup_credentials()
            st.rerun()

if __name__ == "__main__":
    main()
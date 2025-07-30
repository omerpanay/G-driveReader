import streamlit as st
import os
from google_drive.chat_interface import run_drive_chat

def handle_credentials_input():
    """Accepts credentials.json content from the user"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔐 Google API Credentials")
    credentials_content = st.sidebar.text_area(
        "Paste your credentials.json content",
        help="Paste the content of your Google Service Account credentials file"
    )
    if credentials_content:
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
    if 'credentials_path' in st.session_state:
        st.sidebar.success("✅ Credentials already saved")
        return True
    return False

def cleanup_credentials():
    """Deletes the uploaded credentials file"""
    if 'credentials_path' in st.session_state:
        try:
            os.unlink(st.session_state['credentials_path'])
            del st.session_state['credentials_path']
        except:
            pass

def main():
    st.set_page_config(
        page_title="Drive File Reader",
        page_icon="📁",
        layout="wide"
    )
    st.title("📁 Google Drive File Reader")
    st.write("Reads files from a Drive folder.")

    credentials_saved = handle_credentials_input()
    if not credentials_saved:
        st.warning("⚠️ Please enter your Google API credentials.json content.")
        st.info("""
        **How to obtain credentials:**
        1. Go to [Google Cloud Console](https://console.cloud.google.com/)
        2. Create a new project or select an existing one
        3. Enable Google Drive API
        4. Create a Service Account
        5. Download the JSON key file
        6. Paste its content here
        """)
        return

    folder_id = st.text_input("Google Drive Folder ID", help="Enter the folder ID")
    if st.button("📂 Read Files"):
        if not folder_id:
            st.error("Please enter a Drive Folder ID!")
        else:
            try:
                # Call run_drive_chat with the Drive Folder ID
                result = run_drive_chat(folder_id=folder_id)
                st.success("Files successfully read!")
                st.code(result, language="text")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    if st.sidebar.button("🗑️ Clear Credentials"):
        cleanup_credentials()
        st.rerun()

if __name__ == "__main__":
    main()
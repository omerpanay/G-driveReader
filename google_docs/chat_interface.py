import streamlit as st
from shared.llama_utils import setup_llama_index, create_index_from_documents
from shared.config import setup_environment
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Document:
    """Simple document class to replace llama_index Document"""
    def __init__(self, text, metadata=None):
        self.text = text
        self.metadata = metadata or {}

def run_documents_chat(document_id):
    """Reads a specific document from Google Documents"""
    setup_environment()

    # Set up LlamaIndex (simplified)
    setup_llama_index()

    st.title("📄 Google Documents Reader")
    st.write("Reading document from Google Documents...")

    try:
        # Create Google Documents API client
        service = build('docs', 'v1')

        # Get the document by ID
        document = service.documents().get(documentId=document_id).execute()

        if not document:
            st.warning("Document not found.")
            return "Document not found."

        # Process the document and create an index
        content_elements = document.get("body", {}).get("content", [])
        text_content = ""
        
        # Extract text from document structure
        for element in content_elements:
            if "paragraph" in element:
                paragraph = element.get("paragraph", {})
                elements = paragraph.get("elements", [])
                for elem in elements:
                    text_run = elem.get("textRun", {})
                    content = text_run.get("content", "")
                    text_content += content
        
        formatted_document = Document(
            text=text_content,
            metadata={"title": document.get("title", "Unknown Document")}
        )
        
        index = create_index_from_documents([formatted_document])
        st.success("Document successfully read and index created!")

        # Display the document information
        st.write("### Document Information:")
        st.write(f"**Title:** {formatted_document.metadata['title']}")
        st.write(f"**Character Count:** {len(text_content)}")
        
        # Show document content
        st.write("### Document Content:")
        st.text_area("Content", text_content, height=300)
        
        return text_content
        
    except HttpError as e:
        error_msg = f"API error occurred: {e}"
        st.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        st.error(error_msg)
        return error_msg
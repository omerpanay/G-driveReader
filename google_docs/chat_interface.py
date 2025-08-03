import streamlit as st
from shared.llama_utils import setup_llama_index, create_index_from_documents
from shared.config import setup_environment
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from llama_index.core import Document

def run_documents_chat(document_id):
    """Reads a specific document from Google Documents"""
    setup_environment()

    # Set up LlamaIndex
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
            return

        # Process the document and create an index
        content_elements = document.get("body", {}).get("content", [])
        text_content = "".join(
            element.get("paragraph", {}).get("elements", [{}])[0].get("textRun", {}).get("content", "")
            for element in content_elements if "paragraph" in element
        )
        formatted_document = Document(
            text=text_content,
            metadata={"title": document.get("title", "Unknown Document")}
        )
        index = create_index_from_documents([formatted_document])
        st.success("Document successfully read and index created!")

        # Display the list of files read
        st.write("### Files Read:")
        st.write(f"- {formatted_document.metadata['title']}")
    except HttpError as e:
        st.error(f"API error occurred: {e}")
        return
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return
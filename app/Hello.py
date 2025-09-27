"""
Main application entry point for the Widerspruchsassistent.
Handles document upload, processing, and provides navigation to other pages.
"""
import streamlit as st
import tempfile
import os
from pathlib import Path

from ocr_service import OCRService, OCRServiceError
from config import Config
from utils import (
    cleanup_document, 
    clear_all_session_data, 
    initialize_session_state,
    cleanup,
    display_legal_disclaimer,
    display_privacy_notice
)

def setup_page_configuration() -> None:
    """Set up the page configuration."""
    st.set_page_config(
        page_title=Config.APP_TITLE,
        page_icon=Config.APP_ICON,
        layout=Config.PAGE_LAYOUT
    )


def setup_sidebar() -> None:
    """Set up the sidebar with navigation options."""
    st.sidebar.success("Wähle eine Option aus")


def perform_full_cleanup() -> None:
    """Perform a complete cleanup of the application."""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 1: Delete document from Mistral server
    status_text.text("🗑️ Lösche Dokument vom Server...")
    progress_bar.progress(25)
    
    if hasattr(st.session_state, "document") and st.session_state.document is not None:
        try:
            # Direct API call to delete
            from mistralai import Mistral
            client = Mistral(api_key=Config.get_mistral_api_key())
            file_id = st.session_state.document.file_id
            if file_id:
                client.files.delete(file_id=file_id)
                status_text.text("✅ Dokument vom Server gelöscht!")
            else:
                status_text.text("⚠️ Keine File ID gefunden")
        except Exception as e:
            status_text.text(f"❌ Fehler beim Löschen: {str(e)}")
    
    progress_bar.progress(50)
    
    # Step 2: Clear all session state
    status_text.text("🧹 Lösche App-Daten...")
    progress_bar.progress(75)
    
    clear_all_session_data()
    
    # Step 3: Clear file uploader state
    status_text.text("🔄 Setze Upload-Feld zurück...")
    progress_bar.progress(90)
    
    # Force clear the file uploader by setting a flag
    st.session_state.file_uploader_cleared = True
    
    progress_bar.progress(100)
    status_text.text("✅ App erfolgreich zurückgesetzt!")
    
    # Small delay to show the success message
    import time
    time.sleep(1)
    
    # Clear the progress indicators
    progress_bar.empty()
    status_text.empty()
    
    # Refresh the page
    st.rerun()


def display_welcome_content() -> None:
    """Display the welcome content and instructions."""
    st.title("👋 Willkommen zu deinem Widerspruchsassistent!")
    
    display_legal_disclaimer()
    
    # Displaying a markdown header with a welcoming message and description
    st.markdown("""
    Erstellen Sie einen Widerspruch zu Ihrem Schreiben oder lassen Sie sich von unserem Assistenten erklären, 
    was in Ihrem Dokument steht.
    """)


def process_uploaded_file(uploaded_file) -> None:
    """
    Process the uploaded file and create OCR service instance.
    
    Args:
        uploaded_file: The uploaded file object from Streamlit.
    """
    with st.spinner("Dokument wird verarbeitet..."):
        temp_file_path = None
        try:
            # Create a temporary file with a more secure approach
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_file_path = Path(temp_file.name)
            
            # Process the document
            document = OCRService(temp_file_path)
            document.process()
            st.session_state.document = document
            
            # Show success message and delete button
            st.success("Dokument erfolgreich verarbeitet!")
            display_delete_button()
            
        except OCRServiceError as e:
            st.error(f"Fehler bei der Dokumentenverarbeitung: {str(e)}")
        except Exception as e:
            st.error(f"Unerwarteter Fehler: {str(e)}")
        finally:
            # Ensure cleanup even if there's an error
            if temp_file_path and temp_file_path.exists():
                try:
                    os.unlink(temp_file_path)
                except:
                    pass


def display_delete_button() -> None:
    """Display the delete button under the upload field."""
    if st.button("Dokument löschen & App zurücksetzen", 
                help="Löscht das Dokument vom Server und setzt die gesamte App zurück",
                type="primary",
                use_container_width=True):
        perform_full_cleanup()


def display_document_upload_section() -> None:
    """Display the document upload section."""
    # Use a key for the file uploader to control its state
    uploader_key = "file_uploader"
    if hasattr(st.session_state, "file_uploader_cleared") and st.session_state.file_uploader_cleared:
        # Clear the uploader by using a different key
        uploader_key = f"file_uploader_{st.session_state.get('uploader_counter', 0)}"
        st.session_state.uploader_counter = st.session_state.get('uploader_counter', 0) + 1
        del st.session_state.file_uploader_cleared

    uploaded_file = st.file_uploader(
        label="Laden Sie Ihr Schreiben hier hoch",
        type=Config.ALLOWED_FILE_TYPES,
        help=f"Unterstützte Formate: {', '.join(Config.ALLOWED_FILE_TYPES).upper()}. Maximale Dateigröße: {Config.get_max_file_size_mb()} MB",
        key=uploader_key
    )

    # Check if document is already loaded
    if hasattr(st.session_state, "document") and st.session_state.document is not None:
        st.success(f"📄 Dokument geladen: {st.session_state.document.file_path.name}")

    if uploaded_file is not None:
        process_uploaded_file(uploaded_file)

    elif hasattr(st.session_state, "document") and st.session_state.document is not None:
        # Display delete button under the upload field if document exists
        display_delete_button()


def main() -> None:
    """Main application function."""
    setup_page_configuration()
    
    # Initialize session state
    initialize_session_state()
    cleanup()
    
    # Display welcome content
    display_welcome_content()
    
    # Display document upload section
    display_document_upload_section()
    
    
    # Display privacy notice
    display_privacy_notice()


# Run the main application
if __name__ == "__main__":
    main()
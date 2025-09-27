"""
Objection creation page for the Widerspruchsassistent.
Allows users to create legal objections based on their uploaded document.
"""
import streamlit as st

from conversation_service import ConversationService, ConversationServiceError
from config import Config
from utils import cleanup_document, display_legal_disclaimer, display_privacy_notice

def setup_page_configuration() -> None:
    """Set up the page configuration."""
    st.set_page_config(
        page_title=Config.get_objection_creation_page_title(),
        page_icon="📄",
        layout=Config.PAGE_LAYOUT
    )


def display_page_header() -> None:
    """Display the page header and legal disclaimer."""
    st.title(f"📄 {Config.get_objection_creation_page_title()}")
    display_legal_disclaimer()


def get_services_input() -> str:
    """
    Get user input for services/benefits they want to claim.
    
    Returns:
        str: The user's input for services/benefits.
    """
    return st.text_area(
        "Welche Leistungen möchten Sie beanspruchen?", 
        value="",
        height=100,
        help=Config.get_services_input_help(),
        key="services_input"
    )




def display_last_objection() -> None:
    """Display only the last AI response (the objection)."""
    if "messages" in st.session_state and st.session_state.messages:
        # Find the last assistant message
        last_assistant_message = None
        for message in reversed(st.session_state.messages):
            if message["role"] == "assistant":
                last_assistant_message = message
                break
        
        if last_assistant_message:
            st.markdown("### 📄 Ihr Widerspruch:")
            st.markdown(last_assistant_message["content"])


def create_objection_from_services(document, leistungen: str) -> None:
    """Create a new objection based on the services input."""
    if leistungen.strip():
        with st.spinner("Erstelle neuen Widerspruch..."):
            try:
                # Create new conversation service for each objection
                service = ConversationService(document.signed_url)
                response = service.start_conversation(leistungen)
                st.session_state.messages = service.messages
                st.session_state.conversation_service = service
                st.success("✅ Neuer Widerspruch erstellt!")
            except ConversationServiceError as e:
                st.error(f"❌ Fehler beim Erstellen des Widerspruchs: {str(e)}")
                st.session_state.messages = []
            except Exception as e:
                st.error(f"❌ Unerwarteter Fehler: {str(e)}")
                st.session_state.messages = []


def handle_services_input(document) -> None:
    """
    Handle the services input and create objection.
    
    Args:
        document: The document object.
    """
    leistungen = get_services_input()
    
    # Check if document has a valid signed URL
    if not hasattr(document, 'signed_url') or not document.signed_url:
        st.error(f"❌ {Config.get_error_document_processing()}")
        return
    
    # Check if services input has changed
    if leistungen.strip():
        # Check if this is a new input (different from last processed)
        last_processed = st.session_state.get("last_processed_services", "")
        if leistungen != last_processed:
            create_objection_from_services(document, leistungen)
            st.session_state.last_processed_services = leistungen

    # Display the current objection
    display_last_objection()


def main() -> None:
    """Main function for the objection creation page."""
    setup_page_configuration()
    display_page_header()
    
    # Initialize messages if not already present
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Check if document is loaded
    if hasattr(st.session_state, "document") and st.session_state.document is not None:
        document = st.session_state.document
        handle_services_input(document)
    else:
        # Display placeholder when no document is loaded
        st.info("📄 **Kein Dokument geladen**")
        st.markdown("""
        Um einen Widerspruch zu erstellen, müssen Sie zuerst ein Dokument hochladen.
        
        **So geht's:**
        1. Gehen Sie zurück zur Hauptseite
        2. Laden Sie Ihr Dokument hoch (PDF, DOCX oder DOC)
        3. Kehren Sie zu dieser Seite zurück
        
        Ihr Dokument wird dann automatisch verarbeitet und Sie können einen Widerspruch erstellen.
        """)
        
        st.markdown("---")
        st.markdown("### 💡 Was Sie hier tun können:")
        objection_help = Config.get_objection_creation_help()
        if objection_help:
            st.markdown(objection_help)
        else:
            st.markdown("""
            - **Leistungen beschreiben**: Beschreiben Sie die Leistungen, die Sie beantragt haben
            - **Widerspruch erstellen**: Die KI erstellt automatisch einen formellen Widerspruch
            - **Anpassen**: Sie können den Widerspruch nach Ihren Bedürfnissen anpassen
            """)

    display_privacy_notice()


# Run the main function
if __name__ == "__main__":
    main()
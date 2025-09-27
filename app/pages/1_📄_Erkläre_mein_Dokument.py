"""
Document explanation page for the Widerspruchsassistent.
Allows users to view and understand the content of their uploaded document.
"""
import streamlit as st

from config import Config
from utils import cleanup_document, display_legal_disclaimer, display_privacy_notice
from conversation_service import ConversationService, ConversationServiceError

def setup_page_configuration() -> None:
    """Set up the page configuration."""
    st.set_page_config(
        page_title=Config.get_document_explanation_page_title(),
        page_icon="📄",
        layout=Config.PAGE_LAYOUT
    )


def display_page_header() -> None:
    """Display the page header and legal disclaimer."""
    st.title(f"📄 {Config.get_document_explanation_page_title()}")
    display_legal_disclaimer()


def initialize_document_chat(document) -> None:
    """
    Initialize the document chat service with document-focused system prompt.
    
    Args:
        document: The document object containing the signed URL.
    """
    if "document_chat_service" not in st.session_state:
        try:
            # Document-focused system prompt for normal chat
            document_system_prompt = Config.get_document_chat_system_prompt()
            
            service = ConversationService(document.signed_url, document_system_prompt)
            st.session_state.document_chat_service = service
            st.session_state.document_messages = service.messages
        except ConversationServiceError as e:
            st.error(f"❌ Fehler beim Initialisieren des Chats: {str(e)}")
            st.session_state.document_messages = []


def display_document_chat() -> None:
    """Display the document chat interface."""
    st.markdown("### 💬 Chat mit Ihrem Dokument")
    
    # Display chat messages from history (skip system message)
    if "document_messages" in st.session_state and len(st.session_state.document_messages) > 1:
        for message in st.session_state.document_messages[1:]:  # Skip system message
            with st.chat_message(message["role"]):
                # Handle complex message content (first message with document)
                if isinstance(message["content"], list):
                    # Extract just the text part from complex messages
                    text_content = None
                    for item in message["content"]:
                        if item.get("type") == "text":
                            text_content = item.get("text")
                            break
                    if text_content:
                        st.markdown(text_content)
                    else:
                        st.markdown(str(message["content"]))
                else:
                    # Simple text message
                    st.markdown(message["content"])

    # Chat input for questions
    if prompt := st.chat_input("Stellen Sie Fragen zu Ihrem Dokument..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response from document chat service
        try:
            if "document_chat_service" in st.session_state:
                service = st.session_state.document_chat_service
                
                # For the first message, include the document
                if len(service.messages) == 1:  # Only system message exists
                    user_message = {
                        "role": "user", 
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "document_url",
                                "document_url": str(service.document_url)
                            }
                        ]
                    }
                else:
                    user_message = {"role": "user", "content": prompt}
                
                service.messages.append(user_message)
                response = service.get_response()
                
                # Update session state with the complete conversation
                st.session_state.document_messages = service.messages
            else:
                response = "Entschuldigung, der Dokument-Chat ist nicht verfügbar."
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(response)
                
        except ConversationServiceError as e:
            error_response = f"❌ Fehler beim Verarbeiten Ihrer Anfrage: {str(e)}"
            with st.chat_message("assistant"):
                st.markdown(error_response)
            # Add error to service messages and update session state
            if "document_chat_service" in st.session_state:
                st.session_state.document_chat_service.messages.append({"role": "assistant", "content": error_response})
                st.session_state.document_messages = st.session_state.document_chat_service.messages
        except Exception as e:
            error_response = f"❌ Unerwarteter Fehler: {str(e)}"
            with st.chat_message("assistant"):
                st.markdown(error_response)
            # Add error to service messages and update session state
            if "document_chat_service" in st.session_state:
                st.session_state.document_chat_service.messages.append({"role": "assistant", "content": error_response})
                st.session_state.document_messages = st.session_state.document_chat_service.messages


def display_document_contents(document) -> None:
    """
    Display the document contents in an organized way.
    
    Args:
        document: The document object containing the contents.
    """
    if document.contents:
        # Create expandable sections for better readability
        with st.expander("📖 Vollständiger Dokumentinhalt", expanded=False):
            st.info(Config.get_document_processing_info())
            st.markdown(document.contents)
        st.markdown("---")
        
    else:
        st.warning("⚠️ Das Dokument konnte nicht verarbeitet werden oder ist leer.")


def main() -> None:
    """Main function for the document explanation page."""
    setup_page_configuration()
    display_page_header()
    
    # Check if document is loaded
    document = st.session_state.document if hasattr(st.session_state, "document") else None

    if document is not None:
        # Display document contents
        display_document_contents(document)
        
        # Initialize document chat
        initialize_document_chat(document)
        
        # Display chat interface
        display_document_chat()
    else:
        # Display placeholder when no document is loaded
        st.info("📄 **Kein Dokument geladen**")
        st.markdown("""
        Um Ihr Dokument zu erklären, müssen Sie zuerst ein Dokument hochladen.
        
        **So geht's:**
        1. Gehen Sie zurück zur Hauptseite
        2. Laden Sie Ihr Dokument hoch (PDF, DOCX oder DOC)
        3. Kehren Sie zu dieser Seite zurück
        
        Ihr Dokument wird dann automatisch verarbeitet und Sie können Fragen dazu stellen.
        """)
        
        st.markdown("---")
        st.markdown("### 💡 Beispiel-Fragen, die Sie stellen können:")
        example_questions = Config.get_example_questions()
        if example_questions:
            for question in example_questions:
                st.markdown(f"- \"{question}\"")
        else:
            st.markdown("""
            - "Was steht in diesem Dokument?"
            - "Welche Fristen sind wichtig?"
            - "Was bedeutet dieser rechtliche Begriff?"
            - "Welche Schritte muss ich unternehmen?"
            """)

    display_privacy_notice()


# Run the main function
if __name__ == "__main__":
    main()

"""
Utility functions for the Widerspruchsassistent application.
"""
import streamlit as st
from typing import Optional
from config import Config


def cleanup_document() -> bool:
    """
    Clean up document from Mistral server and session state.
    
    Returns:
        bool: True if cleanup was successful or no document to clean, False if error occurred.
    """
    if hasattr(st.session_state, "document") and st.session_state.document is not None:
        try:
            st.session_state.document.delete_from_mistral()
            st.session_state.document = None
            return True
        except Exception as e:
            st.error(f"❌ Fehler beim Löschen des Dokuments: {str(e)}")
            return False
    return True


def clear_all_session_data() -> None:
    """
    Clear all session state variables completely.
    This function clears all session state to reset the application.
    """
    # Get all keys in session state
    keys_to_clear = list(st.session_state.keys())
    
    # Clear all session state variables
    for key in keys_to_clear:
        del st.session_state[key]
    
    # Ensure the uploader counter is reset
    st.session_state.uploader_counter = 0


def initialize_session_state() -> None:
    """
    Initialize required session state variables.
    """
    if "cleanup_needed" not in st.session_state:
        st.session_state.cleanup_needed = False
    if "uploader_counter" not in st.session_state:
        st.session_state.uploader_counter = 0


def cleanup() -> None:
    """
    Check if cleanup is needed from previous page navigation and perform it.
    """
    if (st.session_state.cleanup_needed and 
        hasattr(st.session_state, "document") and 
        st.session_state.document is not None):
        cleanup_document()
        st.session_state.cleanup_needed = False


def display_legal_disclaimer() -> None:
    """Display the legal disclaimer warning."""
    st.warning(Config.get_legal_disclaimer(), icon="⚠️")
    st.markdown("---")


def display_privacy_notice() -> None:
    """Display the privacy notice."""
    st.markdown("---")
    st.markdown(Config.get_privacy_notice())

"""
Configuration management for the Widerspruchsassistent application.
"""
import streamlit as st
from typing import Optional


class Config:
    """Application configuration class."""
    
    # LLM Provider Configuration
    @staticmethod
    def get_llm_provider() -> str:
        """Get the primary LLM provider from Streamlit secrets."""
        return st.secrets.get("LLM_PROVIDER", "mistral")
    
    @staticmethod
    def get_llm_api_key(provider_type: str = None) -> Optional[str]:
        """Get API key for the specified provider."""
        provider = provider_type or Config.get_llm_provider()
        return st.secrets.get(f"{provider.upper()}_API_KEY")
    
    @staticmethod
    def get_llm_model(provider_type: str = None) -> str:
        """Get model name for the specified provider."""
        provider = provider_type or Config.get_llm_provider()
        return st.secrets.get(f"{provider.upper()}_MODEL", Config._get_default_model(provider))
    
    @staticmethod
    def _get_default_model(provider: str) -> str:
        """Get default model for provider."""
        defaults = {
            "mistral": "ministral-8b-latest",
            "openai": "gpt-4o-mini",
            "anthropic": "claude-3-5-sonnet-20241022"
        }
        return defaults.get(provider.lower(), "ministral-8b-latest")
    
    # Mistral AI Configuration (Legacy - for OCR)
    @staticmethod
    def get_mistral_api_key() -> Optional[str]:
        """Get Mistral API key from Streamlit secrets."""
        return st.secrets.get("MISTRAL_API_KEY")
    
    @staticmethod
    def get_mistral_model() -> str:
        """Get Mistral model from Streamlit secrets."""
        return st.secrets.get("MISTRAL_MODEL", "ministral-8b-latest")
    
    @staticmethod
    def get_mistral_ocr_model() -> str:
        """Get Mistral OCR model from Streamlit secrets."""
        return st.secrets.get("MISTRAL_OCR_MODEL", "mistral-ocr-latest")
    
    # Application Configuration
    APP_TITLE: str = "Widerspruchsassistent"
    APP_ICON: str = "🙏"
    PAGE_LAYOUT: str = "wide"
    
    # File Upload Configuration
    ALLOWED_FILE_TYPES: list = ["pdf"]
    
    @staticmethod
    def get_max_file_size_mb() -> int:
        """Get max file size from Streamlit secrets."""
        return int(st.secrets.get("MAX_FILE_SIZE_MB", "10"))
    
    # System Prompts
    @staticmethod
    def get_objection_system_prompt() -> str:
        """Get objection system prompt from Streamlit secrets."""
        return st.secrets.get("OBJECTION_SYSTEM_PROMPT", "")
    
    @staticmethod
    def get_document_chat_system_prompt() -> str:
        """Get document chat system prompt from Streamlit secrets."""
        return st.secrets.get("DOCUMENT_CHAT_SYSTEM_PROMPT", "")
    
    # User Messages
    @staticmethod
    def get_objection_user_message_template() -> str:
        """Get objection user message template from Streamlit secrets."""
        return st.secrets.get("OBJECTION_USER_MESSAGE_TEMPLATE", "")
    
    @staticmethod
    def get_document_chat_initial_message() -> str:
        """Get document chat initial message from Streamlit secrets."""
        return st.secrets.get("DOCUMENT_CHAT_INITIAL_MESSAGE", "")
    
    # UI Messages
    @staticmethod
    def get_legal_disclaimer() -> str:
        """Get legal disclaimer from Streamlit secrets."""
        return st.secrets.get("LEGAL_DISCLAIMER", "")
    
    @staticmethod
    def get_privacy_notice() -> str:
        """Get privacy notice from Streamlit secrets."""
        return st.secrets.get("PRIVACY_NOTICE", "")
    
    # Error Messages
    @staticmethod
    def get_error_no_api_key() -> str:
        """Get no API key error message from Streamlit secrets."""
        return st.secrets.get("ERROR_NO_API_KEY", "MISTRAL_API_KEY not configured")
    
    @staticmethod
    def get_error_no_document() -> str:
        """Get no document error message from Streamlit secrets."""
        return st.secrets.get("ERROR_NO_DOCUMENT", "No document loaded")
    
    @staticmethod
    def get_error_document_processing() -> str:
        """Get document processing error message from Streamlit secrets."""
        return st.secrets.get("ERROR_DOCUMENT_PROCESSING", "Document processing error")
    
    # Page-specific Messages
    @staticmethod
    def get_document_explanation_page_title() -> str:
        """Get document explanation page title from Streamlit secrets."""
        return st.secrets.get("DOCUMENT_EXPLANATION_PAGE_TITLE", "Erkläre mein Dokument")
    
    @staticmethod
    def get_objection_creation_page_title() -> str:
        """Get objection creation page title from Streamlit secrets."""
        return st.secrets.get("OBJECTION_CREATION_PAGE_TITLE", "Erstelle einen Widerspruch")
    
    # Help Text
    @staticmethod
    def get_services_input_help() -> str:
        """Get services input help text from Streamlit secrets."""
        return st.secrets.get("SERVICES_INPUT_HELP", "")
    
    @staticmethod
    def get_document_processing_info() -> str:
        """Get document processing info from Streamlit secrets."""
        return st.secrets.get("DOCUMENT_PROCESSING_INFO", "")
    
    @staticmethod
    def get_example_questions() -> list:
        """Get example questions from Streamlit secrets."""
        return st.secrets.get("EXAMPLE_QUESTIONS", [])
    
    @staticmethod
    def get_objection_creation_help() -> str:
        """Get objection creation help text from Streamlit secrets."""
        return st.secrets.get("OBJECTION_CREATION_HELP", "")
    
    @classmethod
    def validate_config(cls) -> bool:
        """
        Validate that all required configuration is present.
        
        Returns:
            bool: True if configuration is valid, False otherwise.
        """
        # Check primary LLM provider
        provider = cls.get_llm_provider()
        if not cls.get_llm_api_key(provider):
            return False
        
        # Check Mistral for OCR (still required)
        if not cls.get_mistral_api_key():
            return False
            
        return True
    
    @classmethod
    def get_missing_config(cls) -> list[str]:
        """
        Get list of missing configuration items.
        
        Returns:
            list[str]: List of missing configuration keys.
        """
        missing = []
        
        # Check primary LLM provider
        provider = cls.get_llm_provider()
        if not cls.get_llm_api_key(provider):
            missing.append(f"{provider.upper()}_API_KEY")
        
        # Check Mistral for OCR (still required)
        if not cls.get_mistral_api_key():
            missing.append("MISTRAL_API_KEY")
            
        return missing

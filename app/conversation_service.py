from typing import List, Dict, Any, Optional
from config import Config
from llm_providers import LLMService, LLMProviderError


class ConversationServiceError(Exception):
    """Custom exception for conversation service errors."""
    pass


class ConversationService:
    def __init__(self, document_url: str, system_prompt: Optional[str] = None, provider_type: Optional[str] = None):
        """
        Initialize the conversation service with LLM provider.
        
        Args:
            document_url (str): The signed URL of the document to process.
            system_prompt (str, optional): Custom system prompt for the conversation.
            provider_type (str, optional): Override the default LLM provider.
            
        Raises:
            ConversationServiceError: If API key is not set or provider initialization fails.
        """
        try:
            self.llm_service = LLMService(provider_type)
            self.messages: List[Dict[str, Any]] = []
            self.document_url = document_url
            
            # Initialize with custom system prompt or default
            if system_prompt:
                self.messages.append({"role": "system", "content": system_prompt})
            else:
                self._initialize_default_system_prompt()
        except LLMProviderError as e:
            raise ConversationServiceError(f"Failed to initialize LLM service: {str(e)}")
    
    def _initialize_default_system_prompt(self) -> None:
        """Initialize the default system prompt for objection creation."""
        system_prompt = Config.get_objection_system_prompt()
        self.messages.append({"role": "system", "content": system_prompt})
    
    def start_conversation(self, leistungen: str) -> str:
        """
        Start a conversation to create a legal objection (Widerspruch).
        
        Args:
            leistungen (str): The services/benefits that were claimed and denied.
            
        Returns:
            str: The AI's response containing the objection.
            
        Raises:
            ConversationServiceError: If there's an error processing the conversation.
        """
        try:
            user_message_template = Config.get_objection_user_message_template()
            user_message_text = user_message_template.format(leistungen=leistungen)
            
            self.messages.append(
                {"role": "user", "content": [
                        {
                            "type": "text",
                            "text": user_message_text
                        },
                        {
                            "type": "document_url",
                            "document_url": str(self.document_url)
                        }
                    ]
                }
            )

            response = self.get_response()
            return response
        except Exception as e:
            raise ConversationServiceError(f"Error starting conversation: {str(e)}")
    
    def start_document_chat(self) -> str:
        """
        Start a conversation about the document content.
        
        Returns:
            str: The AI's response about the document.
            
        Raises:
            ConversationServiceError: If there's an error processing the conversation.
        """
        try:
            initial_message = Config.get_document_chat_initial_message()
            
            self.messages.append(
                {"role": "user", "content": [
                        {
                            "type": "text",
                            "text": initial_message
                        },
                        {
                            "type": "document_url",
                            "document_url": str(self.document_url)
                        }
                    ]
                }
            )

            response = self.get_response()
            return response
        except Exception as e:
            raise ConversationServiceError(f"Error starting document chat: {str(e)}")

    def get_response(self) -> str:
        """
        Get a response from the LLM provider.
        
        Returns:
            str: The AI's response message.
            
        Raises:
            ConversationServiceError: If there's an error getting the response.
        """
        try:
            # Check if provider supports document URLs for complex messages
            if not self.llm_service.supports_document_urls():
                # Convert complex messages to simple text for providers that don't support document URLs
                simplified_messages = self._simplify_messages_for_provider()
                response = self.llm_service.chat_complete(simplified_messages)
            else:
                # Use original messages for providers that support document URLs
                response = self.llm_service.chat_complete(self.messages)
                
            self.messages.append({"role": "assistant", "content": response})
            return response
        except LLMProviderError as e:
            raise ConversationServiceError(f"Error getting response: {str(e)}")
    
    def _simplify_messages_for_provider(self) -> List[Dict[str, Any]]:
        """
        Simplify messages for providers that don't support document URLs.
        
        Returns:
            List[Dict[str, Any]]: Simplified message list
        """
        simplified_messages = []
        
        for message in self.messages:
            if message["role"] == "system":
                simplified_messages.append(message)
            elif message["role"] == "user":
                if isinstance(message["content"], list):
                    # Extract text content from complex message
                    text_content = None
                    for item in message["content"]:
                        if item.get("type") == "text":
                            text_content = item.get("text")
                            break
                    if text_content:
                        simplified_messages.append({
                            "role": "user",
                            "content": text_content
                        })
                else:
                    simplified_messages.append(message)
            elif message["role"] == "assistant":
                simplified_messages.append(message)
        
        return simplified_messages

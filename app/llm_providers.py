"""
LLM Provider abstraction layer using LangChain.
Supports multiple LLM providers with a unified interface.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import streamlit as st

from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_core.documents import Document
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from config import Config


class LLMProviderError(Exception):
    """Custom exception for LLM provider errors."""
    pass


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, api_key: str, model: str):
        """
        Initialize the LLM provider.
        
        Args:
            api_key: API key for the provider
            model: Model name to use
        """
        self.api_key = api_key
        self.model = model
        self.client = self._create_client()
    
    @abstractmethod
    def _create_client(self) -> BaseLanguageModel:
        """Create the LangChain client for this provider."""
        pass
    
    @abstractmethod
    def chat_complete(self, messages: List[Dict[str, Any]]) -> str:
        """
        Complete a chat conversation.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            str: The AI's response
        """
        pass
    
    @abstractmethod
    def supports_document_urls(self) -> bool:
        """Check if this provider supports document URLs in messages."""
        pass


class MistralProvider(BaseLLMProvider):
    """Mistral AI provider implementation."""
    
    def _create_client(self) -> ChatMistralAI:
        """Create Mistral client."""
        return ChatMistralAI(
            api_key=self.api_key,
            model=self.model,
            temperature=0.1
        )
    
    def chat_complete(self, messages: List[Dict[str, Any]]) -> str:
        """Complete chat with Mistral, handling document URLs."""
        try:
            # Convert messages to LangChain format
            langchain_messages = self._convert_messages(messages)
            
            # Use Mistral's native client for document URL support
            from mistralai import Mistral
            mistral_client = Mistral(api_key=self.api_key)
            
            response = mistral_client.chat.complete(
                model=self.model,
                messages=messages
            )
            
            if not response.choices or not response.choices[0].message.content:
                raise LLMProviderError("Empty response from Mistral model")
            
            content = response.choices[0].message.content
            
            # Handle thinking model response format
            if isinstance(content, list):
                return self._extract_text_from_chunks(content)
            else:
                return content
                
        except Exception as e:
            raise LLMProviderError(f"Mistral chat error: {str(e)}")
    
    def supports_document_urls(self) -> bool:
        """Mistral supports document URLs."""
        return True
    
    def _convert_messages(self, messages: List[Dict[str, Any]]) -> List[BaseMessage]:
        """Convert message format to LangChain format."""
        langchain_messages = []
        for msg in messages:
            if msg["role"] == "system":
                langchain_messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))
        return langchain_messages
    
    def _extract_text_from_chunks(self, chunks) -> str:
        """Extract text content from ThinkChunk objects."""
        extracted_texts = []
        
        for chunk in chunks:
            if hasattr(chunk, 'type') and chunk.type == 'thinking':
                continue
            elif hasattr(chunk, 'type') and chunk.type == 'text':
                if hasattr(chunk, 'text'):
                    extracted_texts.append(chunk.text)
            elif isinstance(chunk, str):
                extracted_texts.append(chunk)
        
        return '\n'.join(extracted_texts) if extracted_texts else ""


class OpenAIProvider(BaseLLMProvider):
    """OpenAI provider implementation."""
    
    def _create_client(self) -> ChatOpenAI:
        """Create OpenAI client."""
        return ChatOpenAI(
            api_key=self.api_key,
            model=self.model,
            temperature=0.1
        )
    
    def chat_complete(self, messages: List[Dict[str, Any]]) -> str:
        """Complete chat with OpenAI."""
        try:
            langchain_messages = self._convert_messages(messages)
            response = self.client.invoke(langchain_messages)
            return response.content
        except Exception as e:
            raise LLMProviderError(f"OpenAI chat error: {str(e)}")
    
    def supports_document_urls(self) -> bool:
        """OpenAI supports document URLs with vision models."""
        return self.model.startswith("gpt-4-vision") or self.model.startswith("gpt-4o")
    
    def _convert_messages(self, messages: List[Dict[str, Any]]) -> List[BaseMessage]:
        """Convert message format to LangChain format."""
        langchain_messages = []
        for msg in messages:
            if msg["role"] == "system":
                langchain_messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))
        return langchain_messages


class AnthropicProvider(BaseLLMProvider):
    """Anthropic provider implementation."""
    
    def _create_client(self) -> ChatAnthropic:
        """Create Anthropic client."""
        return ChatAnthropic(
            api_key=self.api_key,
            model=self.model,
            temperature=0.1
        )
    
    def chat_complete(self, messages: List[Dict[str, Any]]) -> str:
        """Complete chat with Anthropic."""
        try:
            langchain_messages = self._convert_messages(messages)
            response = self.client.invoke(langchain_messages)
            return response.content
        except Exception as e:
            raise LLMProviderError(f"Anthropic chat error: {str(e)}")
    
    def supports_document_urls(self) -> bool:
        """Anthropic supports document URLs with Claude 3.5 Sonnet."""
        return "sonnet" in self.model.lower() or "opus" in self.model.lower()
    
    def _convert_messages(self, messages: List[Dict[str, Any]]) -> List[BaseMessage]:
        """Convert message format to LangChain format."""
        langchain_messages = []
        for msg in messages:
            if msg["role"] == "system":
                langchain_messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))
        return langchain_messages


class LLMProviderFactory:
    """Factory class for creating LLM providers."""
    
    @staticmethod
    def create_provider(provider_type: str, api_key: str, model: str) -> BaseLLMProvider:
        """
        Create an LLM provider instance.
        
        Args:
            provider_type: Type of provider ('mistral', 'openai', 'anthropic')
            api_key: API key for the provider
            model: Model name to use
            
        Returns:
            BaseLLMProvider: Configured provider instance
            
        Raises:
            LLMProviderError: If provider type is not supported
        """
        provider_type = provider_type.lower()
        
        if provider_type == "mistral":
            return MistralProvider(api_key, model)
        elif provider_type == "openai":
            return OpenAIProvider(api_key, model)
        elif provider_type == "anthropic":
            return AnthropicProvider(api_key, model)
        else:
            raise LLMProviderError(f"Unsupported provider type: {provider_type}")


class LLMService:
    """Main service class for LLM operations."""
    
    def __init__(self, provider_type: Optional[str] = None):
        """
        Initialize the LLM service.
        
        Args:
            provider_type: Override the default provider type from config
        """
        self.provider_type = provider_type or Config.get_llm_provider()
        self.api_key = Config.get_llm_api_key(self.provider_type)
        self.model = Config.get_llm_model(self.provider_type)
        
        if not self.api_key:
            raise LLMProviderError(f"No API key configured for {self.provider_type}")
        
        self.provider = LLMProviderFactory.create_provider(
            self.provider_type, 
            self.api_key, 
            self.model
        )
    
    def chat_complete(self, messages: List[Dict[str, Any]]) -> str:
        """
        Complete a chat conversation.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            str: The AI's response
        """
        return self.provider.chat_complete(messages)
    
    def supports_document_urls(self) -> bool:
        """Check if the current provider supports document URLs."""
        return self.provider.supports_document_urls()

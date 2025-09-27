# LLM-Agnostic Widerspruchsassistent

This document explains the LLM-agnostic architecture implemented using LangChain, allowing you to switch between different LLM providers while keeping Mistral for OCR processing.

## Architecture Overview

The application now uses a **hybrid approach**:

- **LLM Operations** (chat, objection generation): LLM-agnostic via LangChain
- **OCR Operations** (document processing): Mistral-specific (proprietary OCR)

## Supported LLM Providers

### 1. Mistral AI (Default)
- **Models**: `ministral-8b-latest`, `mistral-large-latest`
- **Document URLs**: ✅ Supported
- **Best for**: Cost-effective, good German language support

### 2. OpenAI
- **Models**: `gpt-4o-mini`, `gpt-4o`, `gpt-4-vision-preview`
- **Document URLs**: ✅ Supported (vision models only)
- **Best for**: High-quality responses, vision capabilities

### 3. Anthropic
- **Models**: `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`
- **Document URLs**: ✅ Supported (Claude 3.5 Sonnet+)
- **Best for**: Long context, complex reasoning

## Configuration

**Important**: The app runs from the `app/` directory, so all imports are relative to that folder.

### Basic Setup

1. Copy `app/.streamlit/secrets_example.toml` to `app/.streamlit/secrets.toml`
2. Set your primary LLM provider:
   ```toml
   LLM_PROVIDER = "mistral"  # or "openai" or "anthropic"
   ```

3. Configure API keys for your chosen provider:
   ```toml
   # For Mistral
   MISTRAL_API_KEY = "your_mistral_api_key"
   MISTRAL_MODEL = "ministral-8b-latest"
   
   # For OpenAI
   OPENAI_API_KEY = "your_openai_api_key"
   OPENAI_MODEL = "gpt-4o-mini"
   
   # For Anthropic
   ANTHROPIC_API_KEY = "your_anthropic_api_key"
   ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"
   ```

4. **Always configure Mistral** (required for OCR):
   ```toml
   MISTRAL_API_KEY = "your_mistral_api_key"
   MISTRAL_OCR_MODEL = "mistral-ocr-latest"
   ```

### Provider-Specific Configuration

#### Mistral Configuration
```toml
LLM_PROVIDER = "mistral"
MISTRAL_API_KEY = "your_key"
MISTRAL_MODEL = "ministral-8b-latest"  # or "mistral-large-latest"
```

#### OpenAI Configuration
```toml
LLM_PROVIDER = "openai"
OPENAI_API_KEY = "your_key"
OPENAI_MODEL = "gpt-4o-mini"  # or "gpt-4o" for vision
```

#### Anthropic Configuration
```toml
LLM_PROVIDER = "anthropic"
ANTHROPIC_API_KEY = "your_key"
ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"
```

## Code Architecture

### Core Components

1. **`llm_providers.py`**: Provider abstraction layer
   - `BaseLLMProvider`: Abstract base class
   - `MistralProvider`, `OpenAIProvider`, `AnthropicProvider`: Concrete implementations
   - `LLMService`: Main service class

2. **`conversation_service.py`**: Refactored to use LLM abstraction
   - Uses `LLMService` instead of direct Mistral client
   - Handles document URL compatibility automatically

3. **`config.py`**: Updated configuration management
   - Provider-agnostic configuration methods
   - Backward compatibility with existing Mistral config

### Key Features

#### Automatic Provider Detection
```python
# Automatically uses the configured provider
service = ConversationService(document_url)

# Or override for specific use cases
service = ConversationService(document_url, provider_type="openai")
```

#### Document URL Compatibility
The system automatically handles document URL support:
- **Mistral**: Full document URL support
- **OpenAI**: Document URLs with vision models only
- **Anthropic**: Document URLs with Claude 3.5 Sonnet+

#### Fallback Handling
If a provider doesn't support document URLs, the system:
1. Extracts text content from complex messages
2. Uses simplified text-only messages
3. Maintains conversation flow

## Usage Examples

### Switching Providers

```python
# Use default provider (from config)
service = ConversationService(document_url)

# Use specific provider
service = ConversationService(document_url, provider_type="openai")

# Check provider capabilities
if service.llm_service.supports_document_urls():
    print("This provider supports document URLs")
```

### Configuration Validation

```python
from config import Config

# Validate configuration
if Config.validate_config():
    print("Configuration is valid")
else:
    missing = Config.get_missing_config()
    print(f"Missing: {missing}")
```

## Benefits of This Architecture

### ✅ Advantages

1. **Provider Flexibility**: Easy switching between LLM providers
2. **Cost Optimization**: Choose providers based on cost/quality needs
3. **Future-Proofing**: New providers can be added easily
4. **Specialized OCR**: Keep Mistral's superior OCR capabilities
5. **Backward Compatibility**: Existing configurations still work

### ⚠️ Considerations

1. **OCR Dependency**: Still requires Mistral for document processing
2. **Provider Differences**: Different models have different capabilities
3. **Cost Variations**: Different providers have different pricing
4. **Document URL Support**: Not all providers support document URLs equally

## Migration Guide

### From Mistral-Only to LLM-Agnostic

1. **No Breaking Changes**: Existing code continues to work
2. **Optional Migration**: Add new provider configs as needed
3. **Gradual Adoption**: Test new providers alongside existing setup

### Adding New Providers

1. Create new provider class in `llm_providers.py`
2. Add configuration methods in `config.py`
3. Update `LLMProviderFactory.create_provider()`
4. Add to `requirements.txt` if needed

## Troubleshooting

### Common Issues

1. **"No API key configured"**
   - Ensure `LLM_PROVIDER` is set correctly
   - Check that corresponding API key is configured

2. **"Document URL not supported"**
   - Provider doesn't support document URLs
   - System will automatically fall back to text-only mode

3. **"Empty response from AI model"**
   - Check API key validity
   - Verify model name is correct
   - Check provider-specific rate limits

### Debug Mode

Enable debug logging to see provider selection:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Considerations

### Provider Selection Guidelines

- **Mistral**: Best for German text, cost-effective
- **OpenAI**: Best for complex reasoning, vision tasks
- **Anthropic**: Best for long documents, nuanced understanding

### Cost Optimization

- Use `gpt-4o-mini` for cost-effective OpenAI usage
- Use `ministral-8b-latest` for budget-conscious Mistral usage
- Consider provider-specific rate limits and quotas

## Future Enhancements

1. **Streaming Support**: Add streaming responses for better UX
2. **Memory Management**: Implement conversation memory
3. **Provider Load Balancing**: Distribute requests across providers
4. **Custom Models**: Support for fine-tuned models
5. **Advanced OCR**: Integration with other OCR providers

## Conclusion

The LLM-agnostic architecture provides flexibility while maintaining the specialized OCR capabilities that make Mistral valuable for document processing. This hybrid approach gives you the best of both worlds: provider flexibility for chat/objection generation and specialized OCR for document processing.

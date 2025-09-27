# Streamlit Configuration

This directory contains the Streamlit configuration files for the Widerspruchsassistent application.

## secrets.toml

The `secrets.toml` file contains all environment variables and configurable prompts for the application. This file should be configured with your actual values before running the application.

### Required Configuration

1. **MISTRAL_API_KEY**: Your Mistral AI API key (required)
2. **MISTRAL_MODEL**: The Mistral model to use (default: "ministral-8b-latest")
3. **MISTRAL_OCR_MODEL**: The Mistral OCR model to use (default: "mistral-ocr-latest")

### Optional Configuration

All other values in the file have sensible defaults and can be customized as needed:

- **MAX_FILE_SIZE_MB**: Maximum file size for uploads (default: 10)
- **System Prompts**: Customize the AI behavior for different use cases
- **User Messages**: Customize the messages sent to the AI
- **UI Messages**: Customize error messages, disclaimers, and help text
- **Page Titles**: Customize page titles
- **Example Questions**: Customize the example questions shown to users

### Security Note

The `secrets.toml` file contains sensitive information (API keys) and should never be committed to version control. Make sure it's included in your `.gitignore` file.

### Example Configuration

```toml
# Required - Replace with your actual API key
MISTRAL_API_KEY = "your_actual_mistral_api_key_here"

# Optional - Customize as needed
MISTRAL_MODEL = "ministral-8b-latest"
MAX_FILE_SIZE_MB = 10

# Customize prompts
OBJECTION_SYSTEM_PROMPT = """
Your custom objection creation prompt here...
"""

DOCUMENT_CHAT_SYSTEM_PROMPT = """
Your custom document chat prompt here...
"""
```

## Getting Started

1. Copy the `secrets.toml` file
2. Replace `"your_mistral_api_key_here"` with your actual Mistral API key
3. Customize any other values as needed
4. Run the Streamlit application

The application will automatically load all configuration from this file.

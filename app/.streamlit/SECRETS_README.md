# 🔐 Secrets Configuration Guide

This guide explains how to configure the `secrets.toml` file for the LLM-agnostic Widerspruchsassistent.

## 📁 File Structure

```
app/
├── .streamlit/
│   ├── secrets.toml          # Your actual configuration (keep private!)
│   ├── secrets_example.toml  # Template with examples
│   └── SECRETS_README.md     # This guide
```

## 🚀 Quick Setup

1. **Copy the example file:**
   ```bash
   cp app/.streamlit/secrets_example.toml app/.streamlit/secrets.toml
   ```

2. **Edit `secrets.toml` with your actual API keys**

3. **Never commit `secrets.toml` to version control!**

## 🔑 Required Configuration

### Primary LLM Provider

Choose your main LLM provider for chat and objection generation:

```toml
# Options: "mistral", "openai", "anthropic"
LLM_PROVIDER = "mistral"
```

### Mistral Configuration (Always Required)

**Mistral is always required for OCR processing**, even if you use a different provider for chat:

```toml
MISTRAL_API_KEY = "your_actual_mistral_api_key"
MISTRAL_MODEL = "magistral-medium-2509"  # or "ministral-8b-latest"
MISTRAL_OCR_MODEL = "mistral-ocr-latest"
```

**Get your Mistral API key:** https://console.mistral.ai/

### Provider-Specific Configuration

#### Option 1: Mistral (Default)
```toml
LLM_PROVIDER = "mistral"
MISTRAL_API_KEY = "your_mistral_api_key"
MISTRAL_MODEL = "magistral-medium-2509"
```

#### Option 2: OpenAI
```toml
LLM_PROVIDER = "openai"
OPENAI_API_KEY = "your_openai_api_key"
OPENAI_MODEL = "gpt-4o-mini"  # or "gpt-4o" for vision
```

**Get your OpenAI API key:** https://platform.openai.com/api-keys

#### Option 3: Anthropic
```toml
LLM_PROVIDER = "anthropic"
ANTHROPIC_API_KEY = "your_anthropic_api_key"
ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"
```

**Get your Anthropic API key:** https://console.anthropic.com/

## ⚙️ Advanced Configuration

### File Upload Settings
```toml
MAX_FILE_SIZE_MB = 10  # Maximum file size for uploads
```

### System Prompts

Customize the AI's behavior:

```toml
OBJECTION_SYSTEM_PROMPT = """
Du bist ein Experte für deutsche Sozialrecht und Verwaltungsrecht. 
Erstelle präzise, rechtlich korrekte Widersprüche gegen Bescheide von Behörden.
"""

DOCUMENT_CHAT_SYSTEM_PROMPT = """
Du bist ein Experte für deutsche Sozialrecht und Verwaltungsrecht.
Erkläre Dokumente verständlich und beantworte Fragen dazu.
"""
```

### User Interface Messages

Customize the text shown to users:

```toml
LEGAL_DISCLAIMER = """
⚠️ **Rechtlicher Hinweis**: Dieser Assistent erstellt nur Vorschläge für Widersprüche. 
Lassen Sie diese von einem Anwalt prüfen, bevor Sie sie einreichen.
"""

PRIVACY_NOTICE = """
🔒 **Datenschutz**: Ihre Dokumente werden nur zur Verarbeitung verwendet und nicht gespeichert.
"""
```

### Page Titles
```toml
DOCUMENT_EXPLANATION_PAGE_TITLE = "Erkläre mein Dokument"
OBJECTION_CREATION_PAGE_TITLE = "Erstelle einen Widerspruch"
```

### Help Text and Examples
```toml
EXAMPLE_QUESTIONS = [
    "Was steht in diesem Dokument?",
    "Welche Fristen sind wichtig?",
    "Was bedeutet dieser rechtliche Begriff?",
    "Welche Schritte muss ich unternehmen?"
]
```

## 🔒 Security Best Practices

### 1. Keep Secrets Private
- ✅ **DO**: Add `secrets.toml` to `.gitignore`
- ❌ **DON'T**: Commit API keys to version control
- ❌ **DON'T**: Share your `secrets.toml` file

### 2. API Key Management
- Use environment variables for production
- Rotate API keys regularly
- Monitor API usage and costs

### 3. File Permissions
```bash
chmod 600 app/.streamlit/secrets.toml
```

## 🧪 Testing Your Configuration

Use the test script to verify your setup:

```bash
cd app
python test_imports.py
```

This will check:
- ✅ All required packages are installed
- ✅ API keys are configured
- ✅ Provider selection works correctly

## 🚨 Troubleshooting

### Common Issues

#### "No module named 'langchain_mistralai'"
```bash
pip install langchain-mistralai langchain-openai langchain-anthropic mistralai
```

#### "API-Schlüssel nicht konfiguriert"
- Check that your API key is correctly set in `secrets.toml`
- Verify the provider name matches your configuration
- Ensure Mistral API key is always present (required for OCR)

#### "Empty response from AI model"
- Verify API key is valid and has credits
- Check model name is correct
- Review provider-specific rate limits

### Configuration Validation

The app automatically validates your configuration on startup. Missing required keys will be displayed as errors.

## 💰 Cost Optimization

### Provider Cost Comparison (Approximate)

| Provider | Model | Cost per 1M tokens | Best For |
|----------|-------|-------------------|----------|
| Mistral | ministral-8b-latest | $0.25 | Cost-effective, German text |
| Mistral | magistral-medium-2509 | $2.00 | High quality, German text |
| OpenAI | gpt-4o-mini | $0.15 | Cost-effective, general use |
| OpenAI | gpt-4o | $5.00 | High quality, vision |
| Anthropic | claude-3-5-sonnet | $3.00 | Long context, reasoning |

### Tips for Cost Control
- Use `gpt-4o-mini` or `ministral-8b-latest` for cost-effective operation
- Monitor usage through provider dashboards
- Set up usage alerts and limits

## 🔄 Switching Providers

To switch LLM providers:

1. **Update `secrets.toml`:**
   ```toml
   LLM_PROVIDER = "openai"  # Change to your preferred provider
   ```

2. **Add the corresponding API key:**
   ```toml
   OPENAI_API_KEY = "your_openai_api_key"
   ```

3. **Restart the Streamlit app**

The app will automatically use the new provider for chat and objection generation while keeping Mistral for OCR.

## 📞 Support

If you encounter issues:

1. Check this README for common solutions
2. Verify your API keys are valid
3. Test with the `test_imports.py` script
4. Check the main application logs

## 🔗 Useful Links

- [Mistral AI Console](https://console.mistral.ai/)
- [OpenAI Platform](https://platform.openai.com/)
- [Anthropic Console](https://console.anthropic.com/)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)

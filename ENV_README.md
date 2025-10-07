# 🔐 Environment Configuration Guide

This guide explains how to configure the `.env` file for the LLM-agnostic Widerspruchsassistent.

## 📁 File Structure

```
23_RECHTSO/
├── .env                    # Your actual configuration (keep private!)
├── .env.example           # Template with examples
└── ENV_README.md          # This guide
```

## 🚀 Quick Setup

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your actual API keys**

3. **Never commit `.env` to version control!**

## 🔑 Required Configuration

### Primary LLM Provider

Choose your main LLM provider for chat and objection generation:

```bash
# Options: "mistral", "openai", "anthropic"
LLM_PROVIDER=mistral
```

### Mistral Configuration (Always Required)

**Mistral is always required for OCR processing**, even if you use a different provider for chat:

```bash
MISTRAL_API_KEY=your_actual_mistral_api_key
MISTRAL_MODEL=magistral-medium-2509  # or "ministral-8b-latest"
MISTRAL_OCR_MODEL=mistral-ocr-latest
```

**Get your Mistral API key:** https://console.mistral.ai/

### Provider-Specific Configuration

#### Option 1: Mistral (Default)
```bash
LLM_PROVIDER=mistral
MISTRAL_API_KEY=your_mistral_api_key
MISTRAL_MODEL=magistral-medium-2509
```

#### Option 2: OpenAI
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini  # or "gpt-4o" for vision
```

**Get your OpenAI API key:** https://platform.openai.com/api-keys

#### Option 3: Anthropic
```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

**Get your Anthropic API key:** https://console.anthropic.com/

## ⚙️ Advanced Configuration

### File Upload Settings
```bash
MAX_FILE_SIZE_MB=10  # Maximum file size for uploads
```

### System Prompts

Customize the AI behavior for different use cases:

```bash
OBJECTION_SYSTEM_PROMPT="Du bist ein Experte für deutsche Sozialrecht und Verwaltungsrecht. 
Erstelle präzise, rechtlich korrekte Widersprüche gegen Bescheide von Behörden."

DOCUMENT_CHAT_SYSTEM_PROMPT="Du bist ein Experte für deutsche Sozialrecht und Verwaltungsrecht.
Erkläre Dokumente verständlich und beantworte Fragen dazu."
```

### User Message Templates

Customize the messages sent to the AI:

```bash
OBJECTION_USER_MESSAGE_TEMPLATE="Bitte erstelle einen Widerspruch gegen den Bescheid für folgende Leistungen:

{leistungen}

Verwende das hochgeladene Dokument als Grundlage für den Widerspruch."

DOCUMENT_CHAT_INITIAL_MESSAGE="Bitte analysiere dieses Dokument und erkläre mir den Inhalt verständlich."
```

### UI Messages

Customize error messages, disclaimers, and help text:

```bash
LEGAL_DISCLAIMER="⚠️ **Rechtlicher Hinweis**: Dieser Assistent erstellt nur Vorschläge für Widersprüche. 
Lassen Sie diese von einem Anwalt prüfen, bevor Sie sie einreichen."

PRIVACY_NOTICE="🔒 **Datenschutz**: Ihre Dokumente werden nur zur Verarbeitung verwendet und nicht gespeichert."

ERROR_NO_API_KEY="API-Schlüssel nicht konfiguriert"
ERROR_NO_DOCUMENT="Kein Dokument geladen"
ERROR_DOCUMENT_PROCESSING="Fehler bei der Dokumentverarbeitung"
```

### Page Titles

```bash
DOCUMENT_EXPLANATION_PAGE_TITLE="Erkläre mein Dokument"
OBJECTION_CREATION_PAGE_TITLE="Erstelle einen Widerspruch"
```

### Help Text

```bash
SERVICES_INPUT_HELP="Beschreiben Sie die Leistungen, die Sie beantragt haben"
DOCUMENT_PROCESSING_INFO="Das Dokument wurde mit OCR verarbeitet und kann nun analysiert werden."

# Example Questions (comma-separated)
EXAMPLE_QUESTIONS="Was steht in diesem Dokument?,Welche Fristen sind wichtig?,Was bedeutet dieser rechtliche Begriff?,Welche Schritte muss ich unternehmen?"

OBJECTION_CREATION_HELP="- **Leistungen beschreiben**: Beschreiben Sie die Leistungen, die Sie beantragt haben
- **Widerspruch erstellen**: Die KI erstellt automatisch einen formellen Widerspruch
- **Anpassen**: Sie können den Widerspruch nach Ihren Bedürfnissen anpassen"
```

## 🔒 Security Notes

1. **Never commit `.env` to version control** - it contains sensitive API keys
2. **The `.env` file is already included in `.gitignore`**
3. **Use `.env.example` as a template** for sharing configuration structure
4. **Keep your API keys secure** and rotate them regularly

## 🚀 Getting Started

1. Copy `.env.example` to `.env`
2. Replace `your_*_api_key_here` with your actual API keys
3. Customize any other values as needed
4. Run the Streamlit application

The application will automatically load all configuration from the `.env` file using `python-dotenv`.

## 🔧 Environment Variable Format

- **No spaces around the `=` sign**: `KEY=value`
- **No quotes needed** for simple values: `MAX_FILE_SIZE_MB=10`
- **Use quotes for multi-line values**: `PROMPT="Line 1\nLine 2"`
- **Comma-separated lists**: `QUESTIONS="Q1,Q2,Q3"`

## 🐛 Troubleshooting

### Common Issues

1. **API key not working**: Check that the key is correctly set in `.env`
2. **Configuration not loading**: Ensure `.env` file is in the project root
3. **Missing variables**: Check that all required variables are set
4. **Syntax errors**: Verify `.env` file format (no spaces around `=`)

### Validation

The application includes built-in configuration validation. If required variables are missing, you'll see helpful error messages indicating what needs to be configured.

# 🙏 Widerspruchsassistent

**Ein KI-gestützter Assistent für die Erstellung von Widersprüchen gegen Behördenbescheide**

Ein intelligenter Streamlit-basierter Assistent, der Nutzern hilft, rechtlich korrekte Widersprüche gegen Bescheide von Behörden zu erstellen. Das System verwendet LLM-agnostische Architektur mit LangChain und unterstützt mehrere KI-Anbieter.

## 🌟 Features

### 📄 Dokumentenanalyse
- **OCR-Verarbeitung**: Automatische Texterkennung aus PDF-Dokumenten
- **Intelligente Analyse**: KI-gestützte Interpretation von Behördenbescheiden
- **Interaktiver Chat**: Stellen Sie Fragen zu Ihrem Dokument

### ⚖️ Widerspruchserstellung
- **Automatische Generierung**: KI erstellt formelle Widersprüche basierend auf Ihren Angaben
- **Rechtliche Korrektheit**: Spezialisiert auf deutsches Sozial- und Verwaltungsrecht
- **Anpassbare Vorlagen**: Personalisieren Sie Widersprüche nach Ihren Bedürfnissen

### 🔄 LLM-Flexibilität
- **Multi-Provider Support**: Mistral, OpenAI, Anthropic
- **Kosteneffizienz**: Wählen Sie den besten Anbieter für Ihre Bedürfnisse
- **Spezialisierte OCR**: Mistral für optimale Dokumentenverarbeitung

## 🏗️ Architektur

### Hybrid-Ansatz
- **LLM-Operationen** (Chat, Widerspruchserstellung): LLM-agnostisch via LangChain
- **OCR-Operationen** (Dokumentenverarbeitung): Mistral-spezifisch (proprietäre OCR)

### Unterstützte Anbieter

| Anbieter | Modelle | Dokument-URLs | Beste Verwendung |
|----------|--------|---------------|-----------------|
| **Mistral** | `magistral-medium-2509`, `ministral-8b-latest` | ✅ | Kosteneffizient, deutsche Sprache |
| **OpenAI** | `gpt-4o-mini`, `gpt-4o` | ✅ (Vision-Modelle) | Hohe Qualität, Vision-Fähigkeiten |
| **Anthropic** | `claude-3-5-sonnet-20241022` | ✅ | Langer Kontext, komplexe Argumentation |

## 🚀 Installation

### Voraussetzungen
- Python 3.8+
- Streamlit
- API-Schlüssel für gewählte LLM-Anbieter
- Mistral API-Schlüssel (immer erforderlich für OCR)

### 1. Repository klonen
```bash
git clone <repository-url>
cd 23_RECHTSO
```

### 2. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### 3. Konfiguration einrichten
```bash
# Beispiel-Konfiguration kopieren
cp app/.streamlit/secrets_example.toml app/.streamlit/secrets.toml

# secrets.toml mit Ihren API-Schlüsseln bearbeiten
```

### 4. Anwendung starten
```bash
cd app
streamlit run pages/1_📄_Erkläre_mein_Dokument.py
```

## ⚙️ Konfiguration

### Schnelle Einrichtung

1. **Primären LLM-Anbieter wählen:**
   ```toml
   LLM_PROVIDER = "mistral"  # oder "openai" oder "anthropic"
   ```

2. **API-Schlüssel konfigurieren:**
   ```toml
   # Mistral (immer erforderlich für OCR)
   MISTRAL_API_KEY = "ihr_mistral_api_schluessel"
   
   # OpenAI (optional - nur wenn OpenAI verwendet wird)
   OPENAI_API_KEY = "ihr_openai_api_schluessel"
   
   # Anthropic (optional - nur wenn Anthropic verwendet wird)
   ANTHROPIC_API_KEY = "ihr_anthropic_api_schluessel"
   ```

### Detaillierte Konfiguration

Siehe [SECRETS_README.md](app/.streamlit/SECRETS_README.md) für eine vollständige Anleitung zur Konfiguration.

## 📁 Projektstruktur

```
23_RECHTSO/
├── app/                          # Hauptanwendungsverzeichnis
│   ├── .streamlit/              # Streamlit-Konfiguration
│   │   ├── secrets.toml         # Ihre Konfiguration (privat!)
│   │   ├── secrets_example.toml # Konfigurationsvorlage
│   │   └── SECRETS_README.md    # Konfigurationsanleitung
│   ├── pages/                   # Streamlit-Seiten
│   │   ├── 1_📄_Erkläre_mein_Dokument.py
│   │   └── 2_📄_Erstelle_einen_Widerspruch.py
│   ├── config.py                # Konfigurationsverwaltung
│   ├── llm_providers.py         # LLM-Anbieter-Abstraktion
│   ├── conversation_service.py  # Gesprächsservice
│   ├── ocr_service.py          # OCR-Service
│   ├── utils.py                # Hilfsfunktionen
│   └── test_imports.py         # Import-Test-Skript
├── requirements.txt             # Python-Abhängigkeiten
├── README.md                   # Diese Datei
└── LLM_AGNOSTIC_README.md     # Technische Dokumentation
```

## 🎯 Verwendung

### 1. Dokument hochladen
- Gehen Sie zur Hauptseite
- Laden Sie Ihr PDF-Dokument hoch
- Das System verarbeitet es automatisch mit OCR

### 2. Dokument verstehen
- Besuchen Sie "📄 Erkläre mein Dokument"
- Stellen Sie Fragen zu Ihrem Dokument
- Erhalten Sie verständliche Erklärungen

### 3. Widerspruch erstellen
- Besuchen Sie "📄 Erstelle einen Widerspruch"
- Beschreiben Sie die Leistungen, die Sie beantragt haben
- Das System erstellt automatisch einen formellen Widerspruch

## 🔧 Entwicklung

### Lokale Entwicklung

1. **Repository klonen und einrichten:**
   ```bash
   git clone <repository-url>
   cd 23_RECHTSO
   pip install -r requirements.txt
   ```

2. **Konfiguration testen:**
   ```bash
   cd app
   python test_imports.py
   ```

3. **Anwendung im Entwicklungsmodus starten:**
   ```bash
   streamlit run pages/1_📄_Erkläre_mein_Dokument.py --server.runOnSave true
   ```

### Neue LLM-Anbieter hinzufügen

1. **Neuen Anbieter in `llm_providers.py` implementieren:**
   ```python
   class NewProvider(BaseLLMProvider):
       def _create_client(self):
           # Implementierung
       def chat_complete(self, messages):
           # Implementierung
   ```

2. **Konfiguration in `config.py` erweitern**

3. **Factory-Methode aktualisieren**

## 🚨 Wichtige Hinweise

### Rechtlicher Disclaimer
⚠️ **Dieser Assistent erstellt nur Vorschläge für Widersprüche. Lassen Sie diese von einem Anwalt prüfen, bevor Sie sie einreichen.**

### Datenschutz
🔒 **Ihre Dokumente werden nur zur Verarbeitung verwendet und nicht gespeichert.**

### API-Kosten
💰 **Überwachen Sie Ihre API-Nutzung und Kosten bei den jeweiligen Anbietern.**

## 🐛 Fehlerbehebung

### Häufige Probleme

#### "No module named 'langchain_mistralai'"
```bash
pip install langchain-mistralai langchain-openai langchain-anthropic mistralai
```

#### "API-Schlüssel nicht konfiguriert"
- Überprüfen Sie Ihre `secrets.toml`-Datei
- Stellen Sie sicher, dass der Anbieter-Name korrekt ist
- Mistral API-Schlüssel ist immer erforderlich (für OCR)

#### "Empty response from AI model"
- Überprüfen Sie die Gültigkeit Ihres API-Schlüssels
- Kontrollieren Sie Ihr Guthaben bei dem Anbieter
- Überprüfen Sie anbieter-spezifische Ratenlimits

## 🔗 Nützliche Links

- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [Mistral AI Console](https://console.mistral.ai/)
- [OpenAI Platform](https://platform.openai.com/)
- [Anthropic Console](https://console.anthropic.com/)

---

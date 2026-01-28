<div align="center">
  <img> (https://github.com/user-attachments/assets/9d903653-0b10-4fbc-9db8-d78d696294f7) </img>

  
  # Coercive Control Analyzer
  ### Personal Development
  
  <p>A comprehensive, production-ready platform for analyzing patterns of coercive control in documents and digital communications.</p>
</div>

---

A comprehensive tool that helps identify concerning behaviors across various communication platforms including PDFs, WhatsApp, SMS, Discord, Telegram, and generic text conversations.

## ⚠️ Important Notice

This tool is designed to support researchers, domestic violence support organizations, and individuals in identifying patterns of coercive control. If you are experiencing abuse or feel unsafe, please contact:

- **National Domestic Violence Hotline (US)**: 1-800-799-7233
- **Crisis Text Line**: Text HOME to 741741
- **Local authorities or emergency services**

## Features

### Core Analysis Capabilities
- **Universal Message Import System**: 🆕 Support for 12+ messaging platforms with automatic format detection
  - WhatsApp, SMS, Discord, Telegram
  - Facebook Messenger (JSON & HTML), Instagram DMs
  - iMessage (text & CSV exports)
  - Email (EML files) and MBOX archives
  - Generic text with custom regex patterns
  - Auto-detection based on file content and structure
- **Multi-Format Support**: Analyze PDFs, conversation exports, and custom formats
- **Pattern Detection**: Identify abuse indicators across 6 categories:
  - Isolation tactics
  - Emotional abuse and degradation
  - Financial control
  - Threats and intimidation
  - Sexual coercion
  - Digital/tech abuse
- **DARVO Tactics Analysis**: 🆕 Comprehensive detection of DARVO (Deny, Attack, and Reverse Victim and Offender) manipulation patterns
  - **Deny**: Detect minimization, outright denial, and blame-shifting language
  - **Attack**: Identify credibility attacks, character assassination, threats, and gaslighting
  - **Reverse Victim/Offender**: Recognize self-victimization and victim-blaming patterns
  - **Institutional DARVO**: Detect manipulation in legal/court contexts
  - **Child-Focused Patterns**: High-priority detection of child weaponization and custody threats
  - **Severity Scoring**: Quantify risk level (low, medium, high, critical)
  - **Forensic Documentation**: Court-ready summaries with timestamps and evidence chains
  - **Compound Pattern Detection**: Identify systematic DARVO sequences
- **Conversation Analysis**: 
  - Frequency and timing patterns
  - Escalation detection
  - Power dynamics analysis
  - Isolation tactics identification
- **Comprehensive Reporting**: Generate detailed reports in HTML, JSON, or plain text
- **Visualizations**: Charts and graphs for pattern analysis
- **Batch Processing**: Analyze multiple files at once

### Security & Privacy Features
- **Data Encryption**: Encrypt sensitive files with password protection
- **Anonymization**: Automatically anonymize personal information (names, emails, phone numbers, addresses)
- **Secure Storage**: Secure file handling with proper permissions
- **Secure Deletion**: Multi-pass secure file deletion

### Production-Ready Infrastructure
- **Docker Support**: Containerized deployment for easy setup
- **Configuration Management**: Flexible environment-based configuration
- **Enhanced CLI**: Modern command-line interface with Click
- **Comprehensive Testing**: Test coverage for reliability
- **Security Best Practices**: Built with privacy and security in mind

## Installation

### Requirements
- Python 3.9 or higher
- pip package manager

### Standard Installation

```bash
# Clone the repository
git clone https://github.com/Carlymarie992/coercive-control-analysis.git
cd coercive-control-analysis

# Install dependencies
pip install -r requirements.txt
```

### Docker Installation

```bash
# Build the Docker image
docker-compose build

# Run with Docker
docker-compose up
```

## Quick Start

### Analyze a PDF Document

```bash
# Basic analysis
python analyze.py document.pdf

# Using the enhanced CLI
python cli.py analyze document.pdf

# Generate HTML report
python cli.py analyze document.pdf --format html --output report.html
```

### Analyze Conversation Logs

```bash
# WhatsApp chat export
python cli.py analyze chat.txt --platform whatsapp --format html

# Facebook Messenger JSON export
python cli.py analyze messenger.json --platform facebook_json

# Instagram DM export
python cli.py analyze instagram_dms.json --platform instagram

# iMessage text export
python cli.py analyze imessage.txt --platform imessage_txt

# Email archive
python cli.py analyze emails.mbox --platform mbox

# Auto-detect platform (JSON files)
python cli.py analyze discord_export.json

# With anonymization
python cli.py analyze conversation.txt --anonymize
```

### Universal Import System

The tool now features a **universal import handler** that automatically detects and parses messages from any supported platform:

```python
from universal_import_handler import UniversalImportHandler

# Auto-detect and parse any supported format
handler = UniversalImportHandler()
messages = handler.parse_file('conversation.json')  # Platform auto-detected

# Or specify platform explicitly
messages = handler.parse_file('messages.txt', platform='whatsapp')

# Check supported platforms
platforms = handler.get_supported_platforms()
print(f"Supported: {', '.join(platforms)}")
```

### Custom Format Support

For custom message formats, use the **Generic Regex Parser**:

```python
from parsers.generic_regex_parser import GenericRegexParser

# Use predefined template
parser = GenericRegexParser(template='basic_timestamp')
messages = parser.parse_file('custom_chat.txt')

# Or define custom pattern
parser = GenericRegexParser(
    pattern=r'(\d{4}-\d{2}-\d{2})\s*-\s*([^:]+):\s*(.+)',
    timestamp_group=1,
    sender_group=2,
    message_group=3,
    timestamp_format='%Y-%m-%d'
)
messages = parser.parse_file('custom_format.log')

# Preview pattern matching
preview = parser.preview_pattern('custom_format.log', num_lines=10)
```

### Batch Processing

```bash
# Analyze multiple files
python cli.py batch file1.pdf file2.txt file3.json --output-dir reports/

# With anonymization
python cli.py batch *.pdf --anonymize --format html
```

### Security Features

```bash
# Encrypt a file
python cli.py encrypt sensitive.pdf encrypted.pdf.enc

# Decrypt a file
python cli.py decrypt encrypted.pdf.enc decrypted.pdf

# Anonymize a text file
python cli.py anonymize-file conversation.txt --output anonymized.txt
```

## Usage Examples

### Example 1: PDF Analysis

```python
from data_processor import DataProcessor
from report_generator import ReportGenerator

# Process PDF
processor = DataProcessor('document.pdf')
results = processor.process()

# Generate report
report_gen = ReportGenerator()
report_path = report_gen.generate_report(results, format='html')
print(f"Report saved to: {report_path}")
```

### Example 2: Conversation Analysis with DARVO Detection

```python
from conversation_analyzer import ConversationAnalyzer

# Analyze WhatsApp chat
analyzer = ConversationAnalyzer.from_file('whatsapp_chat.txt', platform='whatsapp')

# Get comprehensive analysis including DARVO tactics
summary = analyzer.generate_summary()

# Check for DARVO patterns
darvo_analysis = summary['darvo_tactics']
if darvo_analysis['forensic_summary']['full_darvo_pattern_detected']:
    print("⚠ Complete DARVO pattern detected!")
    print(f"Risk Level: {darvo_analysis['severity_assessment']['risk_level']}")
    
# Check for high-risk child-focused patterns
if darvo_analysis['forensic_summary']['high_risk_indicators']:
    print("🚨 HIGH RISK: Child-focused manipulation detected")

# Check for specific patterns
abuse_patterns = analyzer.analyze_abuse_patterns()
escalation = analyzer.analyze_escalation_patterns()

if escalation['escalation_detected']:
    print("⚠ Escalation pattern detected!")
```

### Example 3: DARVO-Focused Analysis

```python
from darvo_analyzer import DARVOAnalyzer

# Analyze text for DARVO patterns
text = """Your communication text or document content here"""
analyzer = DARVOAnalyzer(text=text)
results = analyzer.analyze_darvo_patterns()

# Access forensic summary
forensic = results['forensic_summary']
print(f"Total messages analyzed: {forensic['total_messages_analyzed']}")
print(f"Full DARVO pattern: {forensic['full_darvo_pattern_detected']}")

# View severity assessment
severity = results['severity_assessment']
print(f"Risk Level: {severity['risk_level']}")
print(f"Severity Score: {severity['total_score']}")

# Get recommendations
for action in forensic['recommended_actions']:
    print(f"• {action}")
```

### Example 4: Data Anonymization

```python
from security.anonymization import DataAnonymizer

anonymizer = DataAnonymizer()

# Anonymize text
text = "Contact me at john@email.com or call 555-1234"
anonymized = anonymizer.anonymize_text(text)
# Output: "Contact me at [EMAIL-a1b2] or call [PHONE-c3d4]"

# Anonymize conversation
anonymized_messages = anonymizer.anonymize_conversation(messages)
```

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Key configuration options:

```env
# Analysis settings
ANALYSIS_THRESHOLD=0.5
MAX_FILE_SIZE_MB=100

# Security
ENABLE_ENCRYPTION=False
ENABLE_ANONYMIZATION=False
ENCRYPTION_KEY=your-key-here

# Output
DEFAULT_REPORT_FORMAT=html
```

### Configuration File

Edit `config.ini` for application settings:

```ini
[analysis]
threshold = 0.5
max_file_size_mb = 100

[security]
enable_encryption = False
enable_anonymization = False

[reports]
default_format = html
```

## API Documentation

### DataProcessor

```python
from data_processor import DataProcessor

processor = DataProcessor(filepath)
results = processor.process(platform='whatsapp')  # For conversations
```

### ConversationAnalyzer

```python
from conversation_analyzer import ConversationAnalyzer

analyzer = ConversationAnalyzer.from_file(filepath, platform='whatsapp')
summary = analyzer.generate_summary()
```

### ReportGenerator

```python
from report_generator import ReportGenerator

report_gen = ReportGenerator(output_dir='output')
report_path = report_gen.generate_report(data, format='html')
```

### Security Modules

```python
from security.encryption import DataEncryptor
from security.anonymization import DataAnonymizer
from security.secure_storage import SecureStorage

# Encryption
encryptor = DataEncryptor()
encrypted_file = encryptor.encrypt_file('sensitive.txt')

# Anonymization
anonymizer = DataAnonymizer()
anonymized_text = anonymizer.anonymize_text(text)

# Secure storage
with SecureStorage() as storage:
    temp_file = storage.create_temp_file(content, encrypt=True)
    # File auto-deleted on exit
```

### File Upload Handler

For web applications and file validation:

```python
from file_upload_handler import FileUploadHandler

handler = FileUploadHandler()

# Validate uploaded file
is_valid, error = handler.validate_file('uploaded_file.json')

# Auto-detect platform with confidence score
detection = handler.detect_platform('uploaded_file.json')
print(f"Platform: {detection['platform']}, Confidence: {detection['confidence']}")

# Process upload
result = handler.process_upload('uploaded_file.json')
if result['success']:
    messages = result['messages']
    print(f"Parsed {result['message_count']} messages")
else:
    print(f"Error: {result['error']}")

# Get supported platforms for UI
platforms = handler.get_supported_platforms()
for platform in platforms:
    print(f"{platform['name']}: {platform['description']}")
```

## Supported Platforms

### Conversation Formats

- **WhatsApp**: `.txt` chat exports
- **SMS**: `.xml` or `.csv` backup files
- **Discord**: `.json` exports
- **Telegram**: `.json` exports
- **Facebook Messenger**: `.json` or `.html` exports
- **Instagram**: `.json` Direct Message exports
- **iMessage**: `.txt` or `.csv` exports
- **Email**: `.eml` files (individual messages)
- **MBOX**: `.mbox` email archive files
- **Generic**: `.txt`, `.log`, `.chat` files with custom regex patterns

### Document Formats

- **PDF**: `.pdf` files
- **Text**: `.txt` files

## Security Guidelines

### Data Handling Best Practices

1. **Never commit sensitive data** to version control
2. **Use encryption** for storing sensitive analysis files
3. **Enable anonymization** when sharing results
4. **Secure delete** files after analysis using the secure deletion feature
5. **Use environment variables** for sensitive configuration
6. **Set proper file permissions** (handled automatically)

### Privacy Considerations

- All analysis is performed **locally** - no data is sent to external services
- Anonymization **replaces** sensitive information, not just redacts it
- Encrypted files require both **password and salt** file for decryption
- Temp files are **securely deleted** by default

### Compliance

This tool is designed with:
- Data protection regulation compliance in mind
- Privacy-first design patterns
- Secure-by-default configuration
- Audit trail capabilities (via logging)

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_analyze.py
```

## Docker Usage

### Build and Run

```bash
# Build the image
docker-compose build

# Run analysis in container
docker-compose run analyzer python cli.py analyze /app/data/input.pdf

# Interactive shell
docker-compose run analyzer bash
```

### Volume Mounts

The Docker setup mounts three directories:
- `./data` → `/app/data` (input files)
- `./output` → `/app/output` (reports)
- `./temp` → `/app/temp` (temporary files)

## Development

### Project Structure

```
coercive-control-analysis/
├── analyze.py              # Legacy CLI (backward compatible)
├── cli.py                  # Enhanced CLI with Click
├── abuse_indicators.py     # Abuse pattern definitions
├── conversation_analyzer.py # Conversation analysis engine
├── data_processor.py       # Unified data processing
├── report_generator.py     # Report generation
├── visualizations.py       # Chart generation
├── exports.py              # Export functionality
├── config/                 # Configuration modules
│   ├── settings.py
│   └── security.py
├── parsers/                # Platform-specific parsers
│   ├── whatsapp_parser.py
│   ├── sms_parser.py
│   ├── discord_parser.py
│   ├── telegram_parser.py
│   └── generic_text_parser.py
├── security/               # Security modules
│   ├── encryption.py
│   ├── anonymization.py
│   └── secure_storage.py
├── assets/                 # Static assets (logos, images)
│   └── logos/              # Official branding logos
├── docs/                   # Documentation
│   └── LOGO_INTEGRATION.md # Logo usage guide
├── tests/                  # Test suite
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
└── requirements.txt        # Python dependencies
```

### Documentation



### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Code style and standards
- Testing requirements
- Pull request process
- Security considerations

### Adding New Parsers

To add support for a new messaging platform:

1. **Create a new parser** in `parsers/` directory:

```python
# parsers/myplatform_parser.py
from datetime import datetime
from typing import List, Dict

class MyPlatformParser:
    def __init__(self):
        self.messages: List[Dict] = []
    
    def parse_file(self, filepath: str) -> List[Dict]:
        # Parse the file and populate self.messages
        # Each message should have: timestamp, sender, text, platform
        return self.messages
    
    def get_message_count(self) -> int:
        return len(self.messages)
    
    def get_senders(self) -> List[str]:
        return list(set(msg['sender'] for msg in self.messages))
```

2. **Register the parser** in `universal_import_handler.py`:

```python
PARSER_MAP = {
    # ... existing parsers ...
    'myplatform': 'parsers.myplatform_parser.MyPlatformParser',
}

EXTENSION_MAP = {
    # ... existing mappings ...
    '.myext': ['myplatform'],
}
```

3. **Add tests** in `tests/test_universal_import.py`

4. **Update CLI** in `cli.py` to include the new platform in the choice list

5. **Document** the new platform in README.md

## Roadmap

- [ ] Web interface for non-technical users
- [ ] Additional language support for international use
- [x] **DARVO tactics analysis** - Comprehensive detection of manipulation patterns
- [x] **Universal message import system** - Support for 12+ messaging platforms
- [x] **Custom regex parser** - Support for any message format
- [ ] Machine learning-based pattern detection
- [ ] Integration with support organization workflows
- [ ] Mobile app for secure data collection
- [ ] Advanced sentiment analysis
- [ ] Timeline visualization improvements
- [ ] PDF export for court-ready forensic reports

## License

This project is licensed under the PROPRIETARY SOFTWARE LICENSE. See the [LICENSE](LICENSE) file for details.

## Support

For support, questions, or contributions:
- **Issues**: [GitHub Issues](https://github.com/Carlymarie992/coercive-control-analysis/issues)
- **Email**: cmcheney92@gmail.com
- **Security Issues**: See [SECURITY.md](SECURITY.md)

## Acknowledgments

This tool is built to support those affected by coercive control and the organizations that help them. It draws from:
- Research on coercive control patterns
- Feedback from domestic violence support organizations
- Privacy and security best practices
- Open-source community contributions

## Disclaimer

This tool is provided for informational and research purposes only. It should not be used as:
- A substitute for professional legal advice
- Evidence in legal proceedings without proper validation
- A diagnostic tool without expert interpretation
- The sole basis for making safety decisions

Always consult with qualified professionals when dealing with abuse situations.

---

## 🚀 Advanced Abuse Pattern Engine (2026 Upgrade)

The Coercive Control Analyzer now features the most powerful abuse pattern engine to date:

- **Fuzzy Matching & Synonym Detection**: Detects subtle, slang, and evolving abuse language using similarity scoring and synonym mapping.
- **Context-Aware Pattern Recognition**: Identifies multi-message cycles, escalation, and repeated tactics for deeper behavioral analysis.
- **Comprehensive Keyword Coverage**: Merges Duluth Power and Control Wheels, NDCC Chapter 12, and modern slang into unified detection categories.
- **Modular & Extensible**: Easily add new patterns, legal definitions, and language updates.
- **Machine Learning Ready**: Hooks for future AI upgrades and advanced behavioral modeling.
- **Court-Ready Documentation**: Forensic summaries with timestamps, evidence chains, and severity scoring.

This engine is designed to help put a stop to coercive control and abuse by empowering survivors, professionals, and advocates with the most advanced detection and reporting tools available.

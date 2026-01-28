# Examples

This directory contains example scripts demonstrating various features of the Coercive Control Analysis tool.

## Universal Import System Examples

### Web UI Example

The `web_ui/file_upload_example.html` file provides a complete HTML/JavaScript interface for uploading conversation files with platform selection.

**Features:**
- Drag-and-drop file upload
- Platform auto-detection
- Manual platform selection
- User-friendly interface

**Usage:** Open `web_ui/file_upload_example.html` in a web browser.

### Python API Examples

**Basic Universal Import:**
```python
from universal_import_handler import UniversalImportHandler

handler = UniversalImportHandler()
messages = handler.parse_file('conversation.json')  # Auto-detects platform
```

**File Upload Handler:**
```python
from file_upload_handler import FileUploadHandler

handler = FileUploadHandler()
is_valid, error = handler.validate_file('uploaded.json')
result = handler.process_upload('uploaded.json')
```

**Custom Regex Parser:**
```python
from parsers.generic_regex_parser import GenericRegexParser

parser = GenericRegexParser(template='basic_timestamp')
messages = parser.parse_file('custom_chat.txt')
```

See the main README for more detailed examples.

## DARVO Analysis Example

The `darvo_analysis_example.py` script demonstrates how to use the DARVO (Deny, Attack, and Reverse Victim and Offender) analyzer to detect manipulation patterns.

### Running the Example

```bash
python examples/darvo_analysis_example.py
```

### What it Demonstrates

1. **Basic DARVO Detection**: Identifies deny, attack, and reverse patterns in messages
2. **Severity Assessment**: Calculates risk levels (low, medium, high, critical)
3. **Child-Focused Patterns**: Detects high-risk patterns involving children
4. **Forensic Summary**: Generates court-ready documentation

### Expected Output

The script will analyze sample messages and display:
- DARVO component counts (Deny, Attack, Reverse)
- Risk level and severity score
- Alerts for complete DARVO patterns
- Child-focused manipulation warnings
- Recommended actions

### Extending the Example

You can modify the `messages` list in the script to analyze your own text patterns. Each message should have:
- `timestamp`: datetime object
- `sender`: string identifier
- `text`: message content
- `platform`: communication platform (optional)

## See Also

- [Main README](../README.md) - Full documentation
- [DARVO Indicators](../darvo_indicators.py) - Pattern definitions
- [DARVO Analyzer](../darvo_analyzer.py) - Implementation details

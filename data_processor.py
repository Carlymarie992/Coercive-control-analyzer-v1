"""Unified data processing pipeline for multiple input formats."""

from pathlib import Path
from typing import Dict, List, Optional
import json

from pypdf import PdfReader
from analyze import normalize_text, analyze_text
from conversation_analyzer import ConversationAnalyzer
from config.settings import (
    SUPPORTED_PDF_EXTENSIONS,
    SUPPORTED_TEXT_EXTENSIONS,
    SUPPORTED_JSON_EXTENSIONS,
    SUPPORTED_CSV_EXTENSIONS,
    MAX_FILE_SIZE_MB
)


class DataProcessor:
    """Unified data processor for handling multiple input formats."""

    def __init__(self, filepath: str):
        """
        Initialize the data processor.

        Args:
            filepath: Path to the input file
        """
        self.filepath = Path(filepath)
        self.file_extension = self.filepath.suffix.lower()
        self.data_type = self._detect_data_type()
        self.raw_data = None
        self.processed_data = None

        # Validate file
        self._validate_file()

    def _validate_file(self):
        """Validate the input file."""
        if not self.filepath.exists():
            raise FileNotFoundError(f"File not found: {self.filepath}")

        # Check file size
        file_size_mb = self.filepath.stat().st_size / (1024 * 1024)
        if file_size_mb > MAX_FILE_SIZE_MB:
            raise ValueError(
                f"File size ({file_size_mb:.2f} MB) exceeds maximum "
                f"allowed size ({MAX_FILE_SIZE_MB} MB)"
            )

    def _detect_data_type(self) -> str:
        """
        Detect the type of data based on file extension.

        Returns:
            Data type: 'pdf', 'text', 'json', 'csv', 'unknown'
        """
        if self.file_extension in SUPPORTED_PDF_EXTENSIONS:
            return 'pdf'
        elif self.file_extension in SUPPORTED_TEXT_EXTENSIONS:
            return 'text'
        elif self.file_extension in SUPPORTED_JSON_EXTENSIONS:
            return 'json'
        elif self.file_extension in SUPPORTED_CSV_EXTENSIONS:
            return 'csv'
        else:
            return 'unknown'

    def process(self, platform: Optional[str] = None) -> Dict:
        """
        Process the input file based on its type.

        Args:
            platform: For conversation files, specify platform
                     (whatsapp, sms, discord, telegram, generic)

        Returns:
            Dictionary containing processed data and analysis
        """
            # Import message normalization
            try:
                from message_normalizer import normalize_messages
            except ImportError:
                normalize_messages = lambda x: x

            if self.data_type == 'pdf':
                return self._process_pdf()
            elif self.data_type in ['text', 'json', 'csv']:
                messages = self._parse_messages()
                messages = normalize_messages(messages)
                analyzer = ConversationAnalyzer(messages)
                self.processed_data = {
                    'analysis_type': 'conversation_analysis',
                    'filepath': str(self.filepath),
                    'analysis': analyzer.analyze(),
                }
            else:
                raise ValueError(f"Unsupported file type: {self.file_extension}")

    def _process_pdf(self) -> Dict:
        """
        Process PDF file.

        Returns:
            Dictionary with PDF analysis results
        """
        # Extract text from PDF
        try:
            reader = PdfReader(str(self.filepath))
            text = ""
            for page in reader.pages:
                result = page.extract_text()
                if result:
                    text += result + "\n"

            if not text:
                raise ValueError("No text could be extracted from PDF")

            # Normalize and analyze text
            normalized_text = normalize_text(text)
            analysis_results = analyze_text(normalized_text)

            return {
                'file_type': 'pdf',
                'filepath': str(self.filepath),
                'total_pages': len(reader.pages),
                'text_length': len(text),
                'abuse_patterns': analysis_results,
                'analysis_type': 'document_analysis'
            }

        except Exception as e:
            raise ValueError(f"Error processing PDF: {e}")

    def _process_conversation(self, platform: Optional[str] = None) -> Dict:
        """
        Process conversation log file.

        Args:
            platform: Platform type for conversation parsing

        Returns:
            Dictionary with conversation analysis results
        """
        try:
            # Create conversation analyzer
            analyzer = ConversationAnalyzer.from_file(
                str(self.filepath),
                platform=platform
            )

            # Generate comprehensive analysis
            summary = analyzer.generate_summary()

            return {
                'file_type': 'conversation',
                'filepath': str(self.filepath),
                'platform': platform or 'auto-detected',
                'message_count': len(analyzer.messages),
                'analysis': summary,
                'analysis_type': 'conversation_analysis'
            }

        except Exception as e:
            raise ValueError(f"Error processing conversation file: {e}")

    def process_batch(self, filepaths: List[str]) -> List[Dict]:
        """
        Process multiple files.

        Args:
            filepaths: List of file paths to process

        Returns:
            List of analysis results
        """
        results = []
        for filepath in filepaths:
            try:
                processor = DataProcessor(filepath)
                result = processor.process()
                results.append(result)
            except Exception as e:
                results.append({
                    'filepath': filepath,
                    'error': str(e),
                    'success': False
                })

        return results

    def get_text_content(self) -> str:
        """
        Get raw text content from the file.

        Returns:
            Extracted text content
        """
        if self.data_type == 'pdf':
            reader = PdfReader(str(self.filepath))
            text = ""
            for page in reader.pages:
                result = page.extract_text()
                if result:
                    text += result + "\n"
            return text
        elif self.data_type == 'text':
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return f.read()
        elif self.data_type == 'json':
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return json.dumps(data, indent=2)
        else:
            return ""

    def export_results(self, results: Dict, output_path: str, format: str = 'json'):
        """
        Export analysis results to file.

        Args:
            results: Analysis results to export
            output_path: Path for output file
            format: Export format (json, txt)
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, default=str)
        elif format == 'txt':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(self._format_results_as_text(results))
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def _format_results_as_text(self, results: Dict) -> str:
        """Format results as human-readable text."""
        lines = []
        lines.append("=" * 80)
        lines.append("COERCIVE CONTROL ANALYSIS REPORT")
        lines.append("=" * 80)
        lines.append(f"\nFile: {results.get('filepath', 'Unknown')}")
        lines.append(f"Type: {results.get('file_type', 'Unknown')}")
        lines.append("")

        if results.get('analysis_type') == 'document_analysis':
            lines.append("DOCUMENT ANALYSIS")
            lines.append("-" * 80)
            abuse_patterns = results.get('abuse_patterns', {})
            if abuse_patterns:
                for category, keywords in abuse_patterns.items():
                    lines.append(f"\n{category}:")
                    lines.append(f"  Found: {', '.join(keywords)}")
                    lines.append(f"  Count: {len(keywords)}")
            else:
                lines.append("No abuse patterns detected.")

        elif results.get('analysis_type') == 'conversation_analysis':
            lines.append("CONVERSATION ANALYSIS")
            lines.append("-" * 80)
            analysis = results.get('analysis', {})

            # Frequency patterns
            freq = analysis.get('frequency_patterns', {})
            lines.append(f"\nTotal Messages: {freq.get('total_messages', 0)}")
            lines.append(f"Time Span: {freq.get('time_span', {}).get('duration_days', 'N/A')} days")

            # Abuse patterns
            abuse = analysis.get('abuse_patterns', {})
            if abuse:
                lines.append("\nAbuse Patterns Detected:")
                for category, data in abuse.items():
                    lines.append(f"  {category}: {data.get('count', 0)} occurrences")

            # Escalation
            escalation = analysis.get('escalation_patterns', {})
            if escalation.get('escalation_detected'):
                lines.append("\n⚠ ESCALATION DETECTED")

        lines.append("\n" + "=" * 80)
        return "\n".join(lines)

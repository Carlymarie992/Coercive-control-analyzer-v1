"""Export functionality for analysis results."""

import json
import csv
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


class Exporter:
    """Export analysis results to various formats."""

    def __init__(self, output_dir: str = 'output'):
        """
        Initialize exporter.

        Args:
            output_dir: Directory for export files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(self, data: Dict, format: str, filename: Optional[str] = None) -> str:
        """
        Export data to specified format.

        Args:
            data: Data to export
            format: Export format (json, csv, txt)
            filename: Custom filename

        Returns:
            Path to exported file
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'export_{timestamp}.{format}'

        output_path = self.output_dir / filename

        if format == 'json':
            return self._export_json(data, output_path)
        elif format == 'csv':
            return self._export_csv(data, output_path)
        elif format == 'txt':
            return self._export_txt(data, output_path)
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def _export_json(self, data: Dict, output_path: Path) -> str:
        """Export to JSON format."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        return str(output_path)

    def _export_csv(self, data: Dict, output_path: Path) -> str:
        """Export to CSV format."""
        # Flatten data for CSV
        rows = []

        if data.get('analysis_type') == 'conversation_analysis':
            analysis = data.get('analysis', {})
            abuse_patterns = analysis.get('abuse_patterns', {})

            for category, pattern_data in abuse_patterns.items():
                messages = pattern_data.get('messages', [])
                for msg in messages:
                    rows.append({
                        'category': category,
                        'keyword': msg.get('keyword', ''),
                        'timestamp': msg.get('timestamp', ''),
                        'sender': msg.get('sender', ''),
                        'text_excerpt': msg.get('text', '')
                    })

        elif data.get('analysis_type') == 'document_analysis':
            abuse_patterns = data.get('abuse_patterns', {})
            for category, keywords in abuse_patterns.items():
                for keyword in keywords:
                    rows.append({
                        'category': category,
                        'keyword': keyword
                    })

        if rows:
            fieldnames = rows[0].keys()
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        else:
            # Create empty CSV with headers
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['category', 'keyword', 'timestamp', 'sender', 'text_excerpt'])

        return str(output_path)

    def _export_txt(self, data: Dict, output_path: Path) -> str:
        """Export to plain text format."""
        lines = []
        lines.append("COERCIVE CONTROL ANALYSIS EXPORT")
        lines.append("=" * 80)
        lines.append(f"Generated: {datetime.now().isoformat()}")
        lines.append(f"File: {data.get('filepath', 'Unknown')}")
        lines.append("")

        # Add JSON representation
        lines.append(json.dumps(data, indent=2, default=str))

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        return str(output_path)

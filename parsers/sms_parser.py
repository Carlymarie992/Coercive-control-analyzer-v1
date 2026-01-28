"""SMS backup parser for XML and CSV formats."""

import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict


class SMSParser:
    """Parser for SMS backup files (XML and CSV formats)."""

    def __init__(self):
        """Initialize the SMS parser."""
        self.messages: List[Dict] = []

    def parse_file(self, filepath: str) -> List[Dict]:
        """
        Parse an SMS backup file (auto-detects format).

        Args:
            filepath: Path to the SMS backup file

        Returns:
            List of message dictionaries
        """
        if filepath.endswith('.xml'):
            return self.parse_xml(filepath)
        elif filepath.endswith('.csv'):
            return self.parse_csv(filepath)
        else:
            raise ValueError("Unsupported SMS file format. Use XML or CSV.")

    def parse_xml(self, filepath: str) -> List[Dict]:
        """
        Parse XML SMS backup (common format from Android backup apps).

        Args:
            filepath: Path to the XML file

        Returns:
            List of message dictionaries
        """
        self.messages = []

        try:
            tree = ET.parse(filepath)
            root = tree.getroot()

            for sms in root.findall('sms'):
                message = {
                    'timestamp': self._parse_timestamp_ms(sms.get('date', '0')),
                    'sender': sms.get('address', 'Unknown'),
                    'text': sms.get('body', ''),
                    'type': 'received' if sms.get('type') == '1' else 'sent',
                    'platform': 'sms'
                }
                self.messages.append(message)

        except Exception as e:
            raise ValueError(f"Error parsing SMS XML file: {e}")

        return self.messages

    def parse_csv(self, filepath: str) -> List[Dict]:
        """
        Parse CSV SMS backup.

        Args:
            filepath: Path to the CSV file

        Returns:
            List of message dictionaries
        """
        self.messages = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Common CSV headers: timestamp, sender, message, type
                    message = {
                        'timestamp': self._parse_timestamp_str(
                            row.get('timestamp', row.get('date', ''))
                        ),
                        'sender': row.get('sender', row.get('address', 'Unknown')),
                        'text': row.get('message', row.get('body', '')),
                        'type': row.get('type', 'unknown'),
                        'platform': 'sms'
                    }
                    self.messages.append(message)

        except Exception as e:
            raise ValueError(f"Error parsing SMS CSV file: {e}")

        return self.messages

    def _parse_timestamp_ms(self, timestamp_str: str) -> datetime:
        """Parse timestamp from milliseconds."""
        try:
            timestamp_ms = int(timestamp_str)
            return datetime.fromtimestamp(timestamp_ms / 1000.0)
        except (ValueError, TypeError):
            return datetime.now()

    def _parse_timestamp_str(self, timestamp_str: str) -> datetime:
        """Parse timestamp from string."""
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%m/%d/%Y %H:%M:%S',
            '%d/%m/%Y %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
        ]

        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue

        return datetime.now()

    def get_message_count(self) -> int:
        """Get total number of parsed messages."""
        return len(self.messages)

    def get_senders(self) -> List[str]:
        """Get unique list of senders."""
        return list(set(msg['sender'] for msg in self.messages))

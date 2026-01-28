"""Telegram chat export parser (JSON format)."""

import json
from datetime import datetime
from typing import List, Dict


class TelegramParser:
    """Parser for Telegram chat exports (JSON format)."""

    def __init__(self):
        """Initialize the Telegram parser."""
        self.messages: List[Dict] = []

    def parse_file(self, filepath: str) -> List[Dict]:
        """
        Parse a Telegram chat export file (JSON format).

        Args:
            filepath: Path to the Telegram JSON export file

        Returns:
            List of message dictionaries
        """
        self.messages = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Telegram export structure
                messages_data = data.get('messages', [])

                for msg in messages_data:
                    # Skip service messages
                    if msg.get('type') == 'service':
                        continue

                    # Extract text from different message types
                    text = self._extract_text(msg)

                    message = {
                        'timestamp': self._parse_timestamp(msg.get('date', '')),
                        'sender': msg.get('from', 'Unknown'),
                        'text': text,
                        'platform': 'telegram',
                        'message_id': msg.get('id', 0)
                    }
                    self.messages.append(message)

        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing Telegram JSON file: {e}")
        except Exception as e:
            raise ValueError(f"Error parsing Telegram file: {e}")

        return self.messages

    def _extract_text(self, msg: Dict) -> str:
        """Extract text from message, handling different content types."""
        text_content = msg.get('text', '')

        # Handle text as string
        if isinstance(text_content, str):
            return text_content

        # Handle text as list of objects (formatted text)
        if isinstance(text_content, list):
            parts = []
            for item in text_content:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict):
                    parts.append(item.get('text', ''))
            return ''.join(parts)

        return ''

    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse Telegram timestamp."""
        formats = [
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d %H:%M:%S',
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

"""iMessage text export parser."""

import re
from datetime import datetime
from typing import List, Dict


class iMessageTxtParser:
    """Parser for iMessage text exports."""

    def __init__(self):
        """Initialize the iMessage text parser."""
        self.messages: List[Dict] = []

    def parse_file(self, filepath: str) -> List[Dict]:
        """
        Parse an iMessage text export file.

        Args:
            filepath: Path to the iMessage text export file

        Returns:
            List of message dictionaries
        """
        self.messages = []
        current_message = None

        # Common iMessage export patterns:
        # [YYYY-MM-DD HH:MM:SS] Sender: Message
        # YYYY-MM-DD HH:MM:SS - Sender: Message
        pattern_1 = r'\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]\s*([^:]+):\s*(.+)'
        pattern_2 = r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s*-\s*([^:]+):\s*(.+)'

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    # Try to parse as a new message
                    match = re.match(pattern_1, line) or re.match(pattern_2, line)

                    if match:
                        # Save previous message if exists
                        if current_message:
                            self.messages.append(current_message)

                        # Create new message
                        timestamp_str, sender, text = match.groups()
                        current_message = {
                            'timestamp': self._parse_timestamp(timestamp_str),
                            'sender': sender.strip(),
                            'text': text.strip(),
                            'platform': 'imessage'
                        }
                    elif current_message:
                        # Continuation of previous message
                        current_message['text'] += '\n' + line

                # Add last message
                if current_message:
                    self.messages.append(current_message)

        except Exception as e:
            raise ValueError(f"Error parsing iMessage file: {e}")

        return self.messages

    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse timestamp from iMessage format."""
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %I:%M:%S %p',
            '%Y/%m/%d %H:%M:%S',
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

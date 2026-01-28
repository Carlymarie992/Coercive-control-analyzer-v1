"""Generic text parser for simple chat logs and text files."""

import re
from datetime import datetime
from typing import List, Dict, Optional


class GenericTextParser:
    """Parser for generic text-based conversation logs."""

    def __init__(self):
        """Initialize the generic text parser."""
        self.messages: List[Dict] = []

    def parse_file(self, filepath: str, pattern: Optional[str] = None) -> List[Dict]:
        """
        Parse a generic text file with conversation logs.

        Args:
            filepath: Path to the text file
            pattern: Optional regex pattern to parse messages
                    Default pattern: [TIMESTAMP] Sender: Message

        Returns:
            List of message dictionaries
        """
        self.messages = []

        # Default pattern: [2024-01-01 12:00:00] John: Hello
        if pattern is None:
            pattern = r'\[([^\]]+)\]\s*([^:]+):\s*(.+)'

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                current_message = None

                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    match = re.match(pattern, line)
                    if match:
                        # Save previous message
                        if current_message:
                            self.messages.append(current_message)

                        # Create new message
                        if len(match.groups()) >= 3:
                            timestamp_str, sender, text = match.groups()[:3]
                            current_message = {
                                'timestamp': self._parse_timestamp(timestamp_str),
                                'sender': sender.strip(),
                                'text': text.strip(),
                                'platform': 'generic'
                            }
                    elif current_message:
                        # Continuation of previous message
                        current_message['text'] += '\n' + line

                # Add last message
                if current_message:
                    self.messages.append(current_message)

        except Exception as e:
            raise ValueError(f"Error parsing text file: {e}")

        return self.messages

    def parse_simple_format(self, filepath: str) -> List[Dict]:
        """
        Parse simple format without timestamps.
        Format: Sender: Message (one per line)

        Args:
            filepath: Path to the text file

        Returns:
            List of message dictionaries
        """
        self.messages = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                line_number = 0
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    line_number += 1
                    # Simple format: Sender: Message
                    if ':' in line:
                        parts = line.split(':', 1)
                        sender = parts[0].strip()
                        text = parts[1].strip()
                    else:
                        sender = 'Unknown'
                        text = line

                    message = {
                        'timestamp': None,
                        'sender': sender,
                        'text': text,
                        'platform': 'generic',
                        'line_number': line_number
                    }
                    self.messages.append(message)

        except Exception as e:
            raise ValueError(f"Error parsing simple text file: {e}")

        return self.messages

    def _parse_timestamp(self, timestamp_str: str) -> Optional[datetime]:
        """Parse timestamp from various formats."""
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%d/%m/%Y %H:%M:%S',
            '%m/%d/%Y %H:%M:%S',
            '%Y-%m-%d %H:%M',
            '%d/%m/%Y %H:%M',
            '%m/%d/%Y %H:%M',
        ]

        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue

        return None

    def get_message_count(self) -> int:
        """Get total number of parsed messages."""
        return len(self.messages)

    def get_senders(self) -> List[str]:
        """Get unique list of senders."""
        return list(set(msg['sender'] for msg in self.messages))

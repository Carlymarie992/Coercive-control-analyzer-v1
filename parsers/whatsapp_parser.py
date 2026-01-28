"""WhatsApp chat export parser."""

import re
from datetime import datetime
from typing import List, Dict, Optional


class WhatsAppParser:
    """Parser for WhatsApp chat exports."""

    # WhatsApp format: [DD/MM/YYYY, HH:MM:SS] Sender: Message
    # Alternative format: DD/MM/YYYY, HH:MM - Sender: Message
    PATTERN_1 = r'\[?(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?)\]?\s*-?\s*([^:]+):\s*(.+)'
    # US format: MM/DD/YYYY, HH:MM - Sender: Message
    PATTERN_2 = r'(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2}(?:\s*[AP]M)?)\s*-\s*([^:]+):\s*(.+)'

    def __init__(self):
        """Initialize the WhatsApp parser."""
        self.messages: List[Dict] = []

    def parse_file(self, filepath: str) -> List[Dict]:
        """
        Parse a WhatsApp chat export file.

        Args:
            filepath: Path to the WhatsApp chat export file

        Returns:
            List of message dictionaries
        """
        self.messages = []
        current_message = None

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    # Try to parse as a new message
                    match = re.match(self.PATTERN_1, line)
                    if not match:
                        match = re.match(self.PATTERN_2, line)

                    if match:
                        # Save previous message if exists
                        if current_message:
                            self.messages.append(current_message)

                        # Create new message
                        date_str, time_str, sender, text = match.groups()
                        current_message = {
                            'timestamp': self._parse_timestamp(date_str, time_str),
                            'sender': sender.strip(),
                            'text': text.strip(),
                            'platform': 'whatsapp'
                        }
                    elif current_message:
                        # Continuation of previous message
                        current_message['text'] += '\n' + line

                # Add last message
                if current_message:
                    self.messages.append(current_message)

        except Exception as e:
            raise ValueError(f"Error parsing WhatsApp file: {e}")

        return self.messages

    def _parse_timestamp(self, date_str: str, time_str: str) -> Optional[datetime]:
        """Parse timestamp from WhatsApp format."""
        formats = [
            '%d/%m/%Y %H:%M:%S',
            '%d/%m/%Y %H:%M',
            '%m/%d/%Y %I:%M %p',
            '%d/%m/%y %H:%M:%S',
            '%d/%m/%y %H:%M',
        ]

        datetime_str = f"{date_str} {time_str}"
        for fmt in formats:
            try:
                return datetime.strptime(datetime_str, fmt)
            except ValueError:
                continue

        return None

    def get_message_count(self) -> int:
        """Get total number of parsed messages."""
        return len(self.messages)

    def get_senders(self) -> List[str]:
        """Get unique list of senders."""
        return list(set(msg['sender'] for msg in self.messages))

"""iMessage CSV export parser."""

import csv
from datetime import datetime
from typing import List, Dict


class iMessageCSVParser:
    """Parser for iMessage CSV exports."""

    def __init__(self):
        """Initialize the iMessage CSV parser."""
        self.messages: List[Dict] = []

    def parse_file(self, filepath: str) -> List[Dict]:
        """
        Parse an iMessage CSV export file.

        Args:
            filepath: Path to the iMessage CSV export file

        Returns:
            List of message dictionaries
        """
        self.messages = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    # Common CSV headers for iMessage exports
                    # timestamp, sender, message, is_from_me, etc.
                    
                    # Get sender
                    sender = row.get('sender', row.get('handle', 'Unknown'))
                    
                    # Determine if message is from user or contact
                    is_from_me = row.get('is_from_me', '0')
                    if is_from_me in ('1', 'true', 'True', 'yes'):
                        sender = 'Me'

                    message = {
                        'timestamp': self._parse_timestamp(
                            row.get('timestamp', row.get('date', ''))
                        ),
                        'sender': sender,
                        'text': row.get('message', row.get('text', '')),
                        'platform': 'imessage'
                    }

                    # Add optional fields
                    if 'is_from_me' in row:
                        message['is_from_me'] = is_from_me == '1'

                    self.messages.append(message)

        except Exception as e:
            raise ValueError(f"Error parsing iMessage CSV file: {e}")

        return self.messages

    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse timestamp from string."""
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%m/%d/%Y %H:%M:%S',
            '%d/%m/%Y %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d %I:%M:%S %p',
        ]

        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue

        # Try parsing as timestamp
        try:
            # Handle Apple's Core Data timestamp (seconds since 2001-01-01)
            timestamp = float(timestamp_str)
            # Apple's reference date is 2001-01-01 00:00:00 UTC
            if timestamp > 1e9:  # Unix timestamp
                return datetime.fromtimestamp(timestamp)
            else:  # Apple Core Data timestamp
                from datetime import timedelta
                apple_epoch = datetime(2001, 1, 1)
                return apple_epoch + timedelta(seconds=timestamp)
        except (ValueError, TypeError):
            pass

        return datetime.now()

    def get_message_count(self) -> int:
        """Get total number of parsed messages."""
        return len(self.messages)

    def get_senders(self) -> List[str]:
        """Get unique list of senders."""
        return list(set(msg['sender'] for msg in self.messages))

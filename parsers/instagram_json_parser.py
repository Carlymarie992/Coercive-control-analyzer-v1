"""Instagram DM JSON export parser."""

import json
from datetime import datetime
from typing import List, Dict


class InstagramJSONParser:
    """Parser for Instagram Direct Message JSON exports."""

    def __init__(self):
        """Initialize the Instagram JSON parser."""
        self.messages: List[Dict] = []

    def parse_file(self, filepath: str) -> List[Dict]:
        """
        Parse an Instagram DM JSON export file.

        Args:
            filepath: Path to the Instagram JSON export file

        Returns:
            List of message dictionaries
        """
        self.messages = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Instagram structure: {participants: [], messages: []}
            messages_data = data.get('messages', [])

            for msg in messages_data:
                # Skip messages without content
                if 'content' not in msg:
                    continue

                message = {
                    'timestamp': self._parse_timestamp(msg.get('timestamp_ms', 0)),
                    'sender': msg.get('sender_name', 'Unknown'),
                    'text': msg.get('content', ''),
                    'platform': 'instagram'
                }

                # Add optional fields
                if 'share' in msg:
                    message['share'] = msg['share']

                self.messages.append(message)

        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing Instagram JSON file: {e}")
        except Exception as e:
            raise ValueError(f"Error parsing Instagram file: {e}")

        return self.messages

    def _parse_timestamp(self, timestamp_ms: int) -> datetime:
        """Parse timestamp from milliseconds."""
        try:
            return datetime.fromtimestamp(timestamp_ms / 1000.0)
        except (ValueError, TypeError):
            return datetime.now()

    def get_message_count(self) -> int:
        """Get total number of parsed messages."""
        return len(self.messages)

    def get_senders(self) -> List[str]:
        """Get unique list of senders."""
        return list(set(msg['sender'] for msg in self.messages))

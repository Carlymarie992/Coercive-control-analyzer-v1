"""Discord chat export parser (JSON format)."""

import json
from datetime import datetime
from typing import List, Dict


class DiscordParser:
    """Parser for Discord chat exports (JSON format)."""

    def __init__(self):
        """Initialize the Discord parser."""
        self.messages: List[Dict] = []

    def parse_file(self, filepath: str) -> List[Dict]:
        """
        Parse a Discord chat export file (JSON format).

        Args:
            filepath: Path to the Discord JSON export file

        Returns:
            List of message dictionaries
        """
        self.messages = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Discord exports can have different structures
                # Try to handle common formats
                if isinstance(data, dict) and 'messages' in data:
                    messages_data = data['messages']
                elif isinstance(data, list):
                    messages_data = data
                else:
                    raise ValueError("Unsupported Discord export format")

                for msg in messages_data:
                    message = {
                        'timestamp': self._parse_timestamp(
                            msg.get('timestamp', msg.get('time', ''))
                        ),
                        'sender': self._get_sender(msg),
                        'text': msg.get('content', msg.get('message', '')),
                        'platform': 'discord',
                        'channel': msg.get('channel', {}).get('name', 'unknown')
                        if isinstance(msg.get('channel'), dict)
                        else msg.get('channel', 'unknown')
                    }
                    self.messages.append(message)

        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing Discord JSON file: {e}")
        except Exception as e:
            raise ValueError(f"Error parsing Discord file: {e}")

        return self.messages

    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse Discord timestamp."""
        formats = [
            '%Y-%m-%dT%H:%M:%S.%f%z',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%dT%H:%M:%SZ',
        ]

        for fmt in formats:
            try:
                # Remove timezone info for simpler handling
                ts = timestamp_str.replace('+00:00', '').replace('Z', '')
                return datetime.strptime(ts, fmt.replace('%z', ''))
            except ValueError:
                continue

        return datetime.now()

    def _get_sender(self, msg: Dict) -> str:
        """Extract sender name from message."""
        author = msg.get('author', {})
        if isinstance(author, dict):
            return author.get('name', author.get('username', 'Unknown'))
        return str(author) if author else 'Unknown'

    def get_message_count(self) -> int:
        """Get total number of parsed messages."""
        return len(self.messages)

    def get_senders(self) -> List[str]:
        """Get unique list of senders."""
        return list(set(msg['sender'] for msg in self.messages))

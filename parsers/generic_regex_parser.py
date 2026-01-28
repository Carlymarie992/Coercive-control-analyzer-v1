"""Generic regex-based message parser for custom formats."""

import re
from datetime import datetime
from typing import List, Dict, Optional


class GenericRegexParser:
    """
    Generic parser using user-defined regex patterns.
    Allows parsing of custom message formats.
    """

    # Default template patterns for common formats
    TEMPLATE_PATTERNS = {
        'basic_timestamp': {
            'pattern': r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s*-\s*([^:]+):\s*(.+)',
            'groups': {'timestamp': 1, 'sender': 2, 'message': 3},
            'timestamp_format': '%Y-%m-%d %H:%M:%S'
        },
        'bracketed_timestamp': {
            'pattern': r'\[([^\]]+)\]\s*([^:]+):\s*(.+)',
            'groups': {'timestamp': 1, 'sender': 2, 'message': 3},
            'timestamp_format': '%Y-%m-%d %H:%M:%S'
        },
        'simple_line': {
            'pattern': r'([^:]+):\s*(.+)',
            'groups': {'sender': 1, 'message': 2},
            'timestamp_format': None
        }
    }

    def __init__(self, pattern: Optional[str] = None, 
                 timestamp_group: int = 1,
                 sender_group: int = 2,
                 message_group: int = 3,
                 timestamp_format: str = '%Y-%m-%d %H:%M:%S',
                 template: Optional[str] = None):
        """
        Initialize the generic regex parser.

        Args:
            pattern: Regex pattern to extract messages
            timestamp_group: Group number for timestamp (0 if none)
            sender_group: Group number for sender
            message_group: Group number for message text
            timestamp_format: strptime format for timestamp
            template: Use a predefined template pattern
        """
        self.messages: List[Dict] = []
        
        # Use template if provided
        if template and template in self.TEMPLATE_PATTERNS:
            template_config = self.TEMPLATE_PATTERNS[template]
            self.pattern = template_config['pattern']
            groups = template_config['groups']
            self.timestamp_group = groups.get('timestamp', 0)
            self.sender_group = groups['sender']
            self.message_group = groups['message']
            self.timestamp_format = template_config.get('timestamp_format')
        else:
            self.pattern = pattern
            self.timestamp_group = timestamp_group
            self.sender_group = sender_group
            self.message_group = message_group
            self.timestamp_format = timestamp_format

        # Compile the pattern
        if self.pattern:
            self.compiled_pattern = re.compile(self.pattern)
        else:
            self.compiled_pattern = None

    def parse_file(self, filepath: str) -> List[Dict]:
        """
        Parse a file using the configured regex pattern.

        Args:
            filepath: Path to the file

        Returns:
            List of message dictionaries

        Raises:
            ValueError: If no pattern is configured
        """
        if not self.compiled_pattern:
            raise ValueError("No regex pattern configured")

        self.messages = []
        current_message = None

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    # Try to match the pattern
                    match = self.compiled_pattern.match(line)

                    if match:
                        # Save previous message if exists
                        if current_message:
                            self.messages.append(current_message)

                        # Extract groups
                        groups = match.groups()
                        
                        # Build message
                        current_message = {
                            'platform': 'generic_regex'
                        }

                        # Extract timestamp if configured
                        if self.timestamp_group > 0 and len(groups) >= self.timestamp_group:
                            timestamp_str = groups[self.timestamp_group - 1]
                            current_message['timestamp'] = self._parse_timestamp(timestamp_str)
                        else:
                            current_message['timestamp'] = datetime.now()

                        # Extract sender
                        if self.sender_group > 0 and len(groups) >= self.sender_group:
                            current_message['sender'] = groups[self.sender_group - 1].strip()
                        else:
                            current_message['sender'] = 'Unknown'

                        # Extract message
                        if self.message_group > 0 and len(groups) >= self.message_group:
                            current_message['text'] = groups[self.message_group - 1].strip()
                        else:
                            current_message['text'] = ''

                    elif current_message:
                        # Continuation of previous message
                        current_message['text'] += '\n' + line

                # Add last message
                if current_message:
                    self.messages.append(current_message)

        except Exception as e:
            raise ValueError(f"Error parsing file with regex: {e}")

        return self.messages

    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse timestamp using configured format."""
        if not self.timestamp_format:
            return datetime.now()

        try:
            return datetime.strptime(timestamp_str, self.timestamp_format)
        except ValueError:
            pass

        # Try common fallback formats
        fallback_formats = [
            '%Y-%m-%d %H:%M:%S',
            '%d/%m/%Y %H:%M:%S',
            '%m/%d/%Y %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%d-%m-%Y %H:%M:%S',
        ]

        for fmt in fallback_formats:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue

        return datetime.now()

    def preview_pattern(self, filepath: str, num_lines: int = 10) -> List[Dict]:
        """
        Preview how the pattern matches on a sample of the file.

        Args:
            filepath: Path to the file
            num_lines: Number of lines to preview

        Returns:
            List of match results with line numbers
        """
        if not self.compiled_pattern:
            return [{'error': 'No pattern configured'}]

        results = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f):
                    if i >= num_lines:
                        break
                    
                    line = line.strip()
                    if not line:
                        continue

                    match = self.compiled_pattern.match(line)
                    
                    result = {
                        'line_number': i + 1,
                        'line': line,
                        'matched': bool(match)
                    }

                    if match:
                        result['groups'] = match.groups()
                    
                    results.append(result)

        except Exception as e:
            results.append({'error': str(e)})

        return results

    def get_message_count(self) -> int:
        """Get total number of parsed messages."""
        return len(self.messages)

    def get_senders(self) -> List[str]:
        """Get unique list of senders."""
        return list(set(msg['sender'] for msg in self.messages))

    @staticmethod
    def get_available_templates() -> List[str]:
        """Get list of available template names."""
        return list(GenericRegexParser.TEMPLATE_PATTERNS.keys())

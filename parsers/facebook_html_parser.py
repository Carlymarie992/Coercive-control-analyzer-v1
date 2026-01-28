"""Facebook HTML export parser."""

import re
from datetime import datetime
from typing import List, Dict
from html.parser import HTMLParser


class FacebookHTMLParser:
    """Parser for Facebook Messenger HTML exports."""

    def __init__(self):
        """Initialize the Facebook HTML parser."""
        self.messages: List[Dict] = []

    def parse_file(self, filepath: str) -> List[Dict]:
        """
        Parse a Facebook Messenger HTML export file.

        Args:
            filepath: Path to the Facebook HTML export file

        Returns:
            List of message dictionaries
        """
        self.messages = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Parse messages from HTML
            # Common pattern: <div class="message">...</div>
            parser = _FacebookHTMLExtractor()
            parser.feed(html_content)
            
            for msg_data in parser.messages:
                message = {
                    'timestamp': msg_data.get('timestamp', datetime.now()),
                    'sender': msg_data.get('sender', 'Unknown'),
                    'text': msg_data.get('text', ''),
                    'platform': 'facebook'
                }
                self.messages.append(message)

        except Exception as e:
            raise ValueError(f"Error parsing Facebook HTML file: {e}")

        return self.messages

    def get_message_count(self) -> int:
        """Get total number of parsed messages."""
        return len(self.messages)

    def get_senders(self) -> List[str]:
        """Get unique list of senders."""
        return list(set(msg['sender'] for msg in self.messages))


class _FacebookHTMLExtractor(HTMLParser):
    """Internal HTML parser for extracting Facebook messages."""

    def __init__(self):
        super().__init__()
        self.messages = []
        self.current_message = {}
        self.current_tag = None
        self.capture_data = False

    def handle_starttag(self, tag, attrs):
        """Handle HTML start tags."""
        attrs_dict = dict(attrs)
        
        # Look for message containers
        if tag == 'div' and 'class' in attrs_dict:
            classes = attrs_dict['class']
            if 'message' in classes or 'msg' in classes:
                self.current_message = {}
                self.current_tag = 'message'

    def handle_data(self, data):
        """Handle text data in HTML."""
        if self.current_tag and data.strip():
            # Simple extraction - look for sender and message patterns
            # This is a basic implementation; real Facebook HTML can be complex
            text = data.strip()
            
            # Try to identify sender (often first bold text or specific class)
            if not self.current_message.get('sender'):
                self.current_message['sender'] = text
            else:
                # Assume it's the message content
                if 'text' not in self.current_message:
                    self.current_message['text'] = text
                else:
                    self.current_message['text'] += ' ' + text

    def handle_endtag(self, tag):
        """Handle HTML end tags."""
        if tag == 'div' and self.current_tag == 'message':
            if self.current_message.get('text'):
                if 'timestamp' not in self.current_message:
                    self.current_message['timestamp'] = datetime.now()
                self.messages.append(self.current_message)
            self.current_message = {}
            self.current_tag = None

"""MBOX email archive parser."""

import mailbox
from datetime import datetime
from typing import List, Dict
import re
from bs4 import BeautifulSoup


class MboxParser:
    """Parser for MBOX email archive files."""

    def __init__(self):
        """Initialize the MBOX parser."""
        self.messages: List[Dict] = []

    def parse_file(self, filepath: str) -> List[Dict]:
        """
        Parse an MBOX email archive file.

        Args:
            filepath: Path to the MBOX file

        Returns:
            List of message dictionaries
        """
        self.messages = []

        try:
            mbox = mailbox.mbox(filepath)

            for msg in mbox:
                message = {
                    'timestamp': self._parse_timestamp(msg.get('Date', '')),
                    'sender': self._clean_email(msg.get('From', 'Unknown')),
                    'text': self._extract_body(msg),
                    'platform': 'email'
                }

                # Add optional fields
                message['subject'] = msg.get('Subject', '')
                message['to'] = self._clean_email(msg.get('To', ''))
                
                if msg.get('Cc'):
                    message['cc'] = self._clean_email(msg.get('Cc', ''))

                self.messages.append(message)

        except Exception as e:
            raise ValueError(f"Error parsing MBOX file: {e}")

        return self.messages

    def _extract_body(self, msg) -> str:
        """Extract email body text."""
        body = ""
        
        if msg.is_multipart():
            # Get all parts
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))

                # Skip attachments
                if "attachment" in content_disposition:
                    continue

                # Get text content
                if content_type == "text/plain":
                    try:
                        payload = part.get_payload(decode=True)
                        if payload:
                            body = payload.decode('utf-8', errors='ignore')
                            break
                    except Exception:
                        pass
                elif content_type == "text/html" and not body:
                    try:
                        payload = part.get_payload(decode=True)
                        if payload:
                            html_body = payload.decode('utf-8', errors='ignore')
                            body = self._html_to_text(html_body)
                    except Exception:
                        pass
        else:
            # Single part message
            try:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode('utf-8', errors='ignore')
            except Exception:
                body = str(msg.get_payload())

        return body.strip()

    def _html_to_text(self, html: str) -> str:
        """Simple HTML to text conversion."""
        # Use an HTML parser to remove script and style elements and extract text
        soup = BeautifulSoup(html, 'html.parser')

        # Remove script and style elements completely
        for tag in soup(['script', 'style']):
            tag.decompose()

        # Extract text content
        text = soup.get_text(separator=' ')

        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _clean_email(self, email_str: str) -> str:
        """Extract clean email address or name."""
        if not email_str:
            return 'Unknown'
        
        # Try to extract email from "Name <email@domain.com>" format
        match = re.search(r'<([^>]+)>', email_str)
        if match:
            return match.group(1)
        
        # Try to extract just the name part
        match = re.match(r'([^<]+)', email_str)
        if match:
            return match.group(1).strip()
        
        return email_str.strip()

    def _parse_timestamp(self, date_str: str) -> datetime:
        """Parse email date header."""
        if not date_str:
            return datetime.now()

        try:
            # Use email.utils to parse RFC 2822 date
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(date_str)
        except Exception:
            pass

        # Fallback formats
        formats = [
            '%a, %d %b %Y %H:%M:%S %z',
            '%d %b %Y %H:%M:%S %z',
            '%Y-%m-%d %H:%M:%S',
        ]

        for fmt in formats:
            try:
                # Remove timezone info for simpler handling
                clean_date = re.sub(r'\s*\([^)]+\)', '', date_str)
                return datetime.strptime(clean_date.strip(), fmt.replace(' %z', ''))
            except ValueError:
                continue

        return datetime.now()

    def get_message_count(self) -> int:
        """Get total number of parsed messages."""
        return len(self.messages)

    def get_senders(self) -> List[str]:
        """Get unique list of senders."""
        return list(set(msg['sender'] for msg in self.messages))

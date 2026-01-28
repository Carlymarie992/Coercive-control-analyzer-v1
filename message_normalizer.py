from datetime import datetime
import re
from typing import Dict, Any

def normalize_sender(sender: str) -> str:
    """Normalize sender ID by stripping whitespace and handling aliases."""
    if not sender:
        return 'Unknown'
    sender = sender.strip()
    # Optionally, add more alias handling here
    return sender

def normalize_text(text: str) -> str:
    """Clean message contents by removing artifacts and normalizing whitespace."""
    if not text:
        return ''
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def normalize_timestamp(ts: Any) -> Any:
    """Normalize timestamp to datetime or None."""
    if isinstance(ts, datetime):
        return ts
    if isinstance(ts, str):
        formats = [
            '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%d/%m/%Y %H:%M:%S',
            '%m/%d/%Y %H:%M:%S', '%Y-%m-%d %H:%M', '%d/%m/%Y %H:%M', '%m/%d/%Y %H:%M'
        ]
        for fmt in formats:
            try:
                return datetime.strptime(ts, fmt)
            except ValueError:
                continue
    return None

def normalize_message(msg: Dict) -> Dict:
    """Apply normalization to a parsed message dict."""
    msg['sender'] = normalize_sender(msg.get('sender', ''))
    msg['text'] = normalize_text(msg.get('text', ''))
    msg['timestamp'] = normalize_timestamp(msg.get('timestamp', None))
    return msg

def normalize_messages(messages: list) -> list:
    """Normalize a list of message dicts."""
    return [normalize_message(m) for m in messages]

"""Comprehensive conversation analysis module for detecting patterns of coercive control."""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict, Counter
import re

from abuse_indicators import ABUSE_INDICATORS
from parsers.whatsapp_parser import WhatsAppParser
from parsers.sms_parser import SMSParser
from parsers.discord_parser import DiscordParser
from parsers.telegram_parser import TelegramParser
from parsers.generic_text_parser import GenericTextParser
from darvo_analyzer import DARVOAnalyzer
from universal_import_handler import UniversalImportHandler


class ConversationAnalyzer:
    """Analyze conversation logs for patterns of coercive control."""

    def __init__(self, messages: List[Dict]):
        """
        Initialize the conversation analyzer.

        Args:
            messages: List of message dictionaries with keys:
                     timestamp, sender, text, platform
        """
        # Example usage of message normalization
        try:
            from message_normalizer import normalize_messages
            messages = normalize_messages(messages)
        except ImportError:
            pass
        self.messages = sorted(messages, key=lambda x: x.get('timestamp') or datetime.min)
        self.abuse_patterns = {}
        self.sender_stats = {}
        self.timeline_analysis = {}

    @classmethod
    def from_file(cls, filepath: str, platform: Optional[str] = None):
        """
        Create analyzer from a conversation file.

        Args:
            filepath: Path to the conversation file
            platform: Platform type (whatsapp, sms, discord, telegram, generic, etc.)
                     If None, attempts to auto-detect
                     Supports all platforms in UniversalImportHandler

        Returns:
            ConversationAnalyzer instance
        """
        # Use UniversalImportHandler for parsing
        import_handler = UniversalImportHandler()
        
        try:
            # Parse file with universal handler
            messages = import_handler.parse_file(filepath, platform)
            return cls(messages)
        except ValueError:
            # Fallback to legacy parser map for backward compatibility
            if platform is None:
                platform = cls._detect_platform(filepath)

            parser_map = {
                'whatsapp': WhatsAppParser,
                'sms': SMSParser,
                'discord': DiscordParser,
                'telegram': TelegramParser,
                'generic': GenericTextParser,
            }

            parser_class = parser_map.get(platform.lower())
            if not parser_class:
                raise ValueError(f"Unsupported platform: {platform}")

            parser = parser_class()
            messages = parser.parse_file(filepath)

            return cls(messages)

    @staticmethod
    def _detect_platform(filepath: str) -> str:
        """Auto-detect conversation platform from file."""
        if filepath.endswith('.json'):
            # Try to determine if Discord or Telegram
            try:
                import json
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if 'messages' in data and isinstance(data.get('messages'), list):
                        # Check for Telegram-specific fields
                        if data['messages'] and 'from' in data['messages'][0]:
                            return 'telegram'
                        return 'discord'
            except Exception:
                pass
            return 'discord'  # Default for JSON
        elif filepath.endswith('.xml'):
            return 'sms'
        elif filepath.endswith('.csv'):
            return 'sms'
        else:
            # Default to generic for .txt or other text files
            return 'generic'

    def analyze_abuse_patterns(self) -> Dict:
        """
        Scan messages for abuse indicators.

        Returns:
            Dictionary of abuse patterns found
        """
        self.abuse_patterns = {}

        for message in self.messages:
            text = message.get('text', '')
            sender = message.get('sender', 'Unknown')

            # Analyze text for abuse indicators
            for category, keywords in ABUSE_INDICATORS.items():
                for keyword in keywords:
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                    if re.search(pattern, text, re.IGNORECASE):
                        if category not in self.abuse_patterns:
                            self.abuse_patterns[category] = {
                                'keywords': [],
                                'count': 0,
                                'senders': set(),
                                'messages': []
                            }

                        self.abuse_patterns[category]['keywords'].append(keyword)
                        self.abuse_patterns[category]['count'] += 1
                        self.abuse_patterns[category]['senders'].add(sender)
                        self.abuse_patterns[category]['messages'].append({
                            'timestamp': message.get('timestamp'),
                            'sender': sender,
                            'text': text[:100] + '...' if len(text) > 100 else text,
                            'keyword': keyword
                        })

        # Convert sets to lists for JSON serialization
        for category in self.abuse_patterns:
            self.abuse_patterns[category]['senders'] = list(
                self.abuse_patterns[category]['senders']
            )

        return self.abuse_patterns

    def analyze_frequency_patterns(self) -> Dict:
        """
        Analyze message frequency and timing patterns.

        Returns:
            Dictionary with frequency analysis
        """
        if not self.messages:
            return {}

        # Count messages per sender
        sender_counts = Counter(msg['sender'] for msg in self.messages)

        # Analyze time gaps between messages
        time_gaps = []
        for i in range(1, len(self.messages)):
            if (self.messages[i].get('timestamp') and
                    self.messages[i - 1].get('timestamp')):
                gap = (self.messages[i]['timestamp'] -
                       self.messages[i - 1]['timestamp']).total_seconds() / 60
                time_gaps.append(gap)

        # Calculate statistics
        avg_gap = sum(time_gaps) / len(time_gaps) if time_gaps else 0

        # Identify rapid messaging patterns (potential harassment)
        rapid_messages = sum(1 for gap in time_gaps if gap < 1)  # Less than 1 minute

        return {
            'total_messages': len(self.messages),
            'sender_counts': dict(sender_counts),
            'average_time_gap_minutes': round(avg_gap, 2),
            'rapid_message_sequences': rapid_messages,
            'time_span': self._calculate_time_span()
        }

    def analyze_escalation_patterns(self) -> Dict:
        """
        Detect escalation patterns in conversations.

        Returns:
            Dictionary with escalation analysis
        """
        # Group messages by time windows
        if not self.messages or not self.messages[0].get('timestamp'):
            return {'escalation_detected': False, 'details': []}

        window_size = timedelta(days=7)
        current_window_start = self.messages[0]['timestamp']
        window_counts = defaultdict(lambda: defaultdict(int))

        for msg in self.messages:
            if not msg.get('timestamp'):
                continue

            # Move window if needed
            while msg['timestamp'] > current_window_start + window_size:
                current_window_start += window_size

            # Count abuse indicators in this window
            text = msg.get('text', '')
            for category in ['Threats / Intimidation', 'Emotional Abuse / Degradation']:
                for keyword in ABUSE_INDICATORS.get(category, []):
                    if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
                        window_counts[current_window_start][category] += 1

        # Detect escalation (increasing counts over time)
        escalation_detected = False
        details = []

        for category in ['Threats / Intimidation', 'Emotional Abuse / Degradation']:
            counts = [window_counts[w][category] for w in sorted(window_counts.keys())]
            if len(counts) >= 2 and counts[-1] > counts[0]:
                escalation_detected = True
                details.append({
                    'category': category,
                    'trend': 'increasing',
                    'windows': len(counts),
                    'initial_count': counts[0],
                    'final_count': counts[-1]
                })

        return {
            'escalation_detected': escalation_detected,
            'details': details
        }

    def analyze_isolation_tactics(self) -> Dict:
        """
        Analyze patterns indicating isolation tactics.

        Returns:
            Dictionary with isolation analysis
        """
        isolation_keywords = ABUSE_INDICATORS.get('Isolation', [])
        isolation_count = 0
        isolation_messages = []

        for msg in self.messages:
            text = msg.get('text', '')
            for keyword in isolation_keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
                    isolation_count += 1
                    isolation_messages.append({
                        'timestamp': msg.get('timestamp'),
                        'sender': msg.get('sender'),
                        'keyword': keyword,
                        'excerpt': text[:100]
                    })
                    break  # Count each message only once

        return {
            'isolation_indicators_found': isolation_count,
            'severity': 'high' if isolation_count > 10 else 'medium' if isolation_count > 5 else 'low',
            'sample_messages': isolation_messages[:5]  # Show up to 5 examples
        }

    def analyze_power_dynamics(self) -> Dict:
        """
        Analyze power dynamics through communication patterns.

        Returns:
            Dictionary with power dynamics analysis
        """
        sender_stats = defaultdict(lambda: {
            'message_count': 0,
            'avg_message_length': 0,
            'question_count': 0,
            'command_count': 0,
            'total_length': 0
        })

        for msg in self.messages:
            sender = msg.get('sender', 'Unknown')
            text = msg.get('text', '')

            sender_stats[sender]['message_count'] += 1
            sender_stats[sender]['total_length'] += len(text)

            # Count questions
            if '?' in text:
                sender_stats[sender]['question_count'] += 1

            # Detect commands (imperative sentences)
            command_patterns = [
                r'\bdon\'t\b', r'\bstop\b', r'\bcome\b', r'\bgo\b',
                r'\btell me\b', r'\bshow me\b', r'\bgive me\b'
            ]
            if any(re.search(p, text, re.IGNORECASE) for p in command_patterns):
                sender_stats[sender]['command_count'] += 1

        # Calculate averages
        for sender in sender_stats:
            stats = sender_stats[sender]
            if stats['message_count'] > 0:
                stats['avg_message_length'] = stats['total_length'] / stats['message_count']
            del stats['total_length']  # Remove intermediate calculation

        return {
            'sender_statistics': dict(sender_stats),
            'imbalance_detected': self._detect_power_imbalance(sender_stats)
        }

    def _detect_power_imbalance(self, sender_stats: Dict) -> bool:
        """Detect if there's a significant power imbalance."""
        if len(sender_stats) < 2:
            return False

        # Check for significant imbalance in message counts
        counts = [s['message_count'] for s in sender_stats.values()]
        max_count = max(counts)
        min_count = min(counts)

        # If one sender has 3x or more messages, it's an imbalance
        return max_count >= 3 * min_count if min_count > 0 else True

    def _calculate_time_span(self) -> Dict:
        """Calculate the time span of the conversation."""
        if not self.messages:
            return {}

        timestamped = [m for m in self.messages if m.get('timestamp')]
        if not timestamped:
            return {}

        start = min(m['timestamp'] for m in timestamped)
        end = max(m['timestamp'] for m in timestamped)
        duration = end - start

        return {
            'start': start.isoformat() if start else None,
            'end': end.isoformat() if end else None,
            'duration_days': duration.days
        }

    def analyze_darvo_tactics(self) -> Dict:
        """
        Analyze DARVO (Deny, Attack, Reverse Victim/Offender) manipulation tactics.

        Returns:
            Dictionary with DARVO analysis results
        """
        darvo_analyzer = DARVOAnalyzer(messages=self.messages)
        return darvo_analyzer.analyze_darvo_patterns()

    def generate_summary(self) -> Dict:
        """
        Generate a comprehensive summary of all analyses.

        Returns:
            Dictionary with complete analysis summary
        """
        return {
            'abuse_patterns': self.analyze_abuse_patterns(),
            'frequency_patterns': self.analyze_frequency_patterns(),
            'escalation_patterns': self.analyze_escalation_patterns(),
            'isolation_tactics': self.analyze_isolation_tactics(),
            'power_dynamics': self.analyze_power_dynamics(),
            'darvo_tactics': self.analyze_darvo_tactics()
        }

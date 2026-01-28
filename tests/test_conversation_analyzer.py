"""Tests for conversation analyzer module."""

import unittest
from datetime import datetime
from conversation_analyzer import ConversationAnalyzer


class TestConversationAnalyzer(unittest.TestCase):
    """Test conversation analysis functionality."""

    def setUp(self):
        """Set up test data."""
        self.messages = [
            {
                'timestamp': datetime(2024, 1, 1, 10, 0),
                'sender': 'Alice',
                'text': 'Hello, how are you?',
                'platform': 'test'
            },
            {
                'timestamp': datetime(2024, 1, 1, 10, 5),
                'sender': 'Bob',
                'text': "You're stupid and worthless.",
                'platform': 'test'
            },
            {
                'timestamp': datetime(2024, 1, 1, 10, 10),
                'sender': 'Bob',
                'text': "Don't talk to your friends.",
                'platform': 'test'
            }
        ]

    def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = ConversationAnalyzer(self.messages)
        self.assertEqual(len(analyzer.messages), 3)

    def test_abuse_pattern_detection(self):
        """Test abuse pattern detection."""
        analyzer = ConversationAnalyzer(self.messages)
        patterns = analyzer.analyze_abuse_patterns()

        # Should detect emotional abuse
        self.assertIn('Emotional Abuse / Degradation', patterns)
        self.assertGreater(patterns['Emotional Abuse / Degradation']['count'], 0)

        # Should detect isolation
        self.assertIn('Isolation', patterns)

    def test_frequency_analysis(self):
        """Test frequency pattern analysis."""
        analyzer = ConversationAnalyzer(self.messages)
        freq = analyzer.analyze_frequency_patterns()

        self.assertEqual(freq['total_messages'], 3)
        self.assertIn('Alice', freq['sender_counts'])
        self.assertIn('Bob', freq['sender_counts'])

    def test_empty_messages(self):
        """Test with empty message list."""
        analyzer = ConversationAnalyzer([])
        patterns = analyzer.analyze_abuse_patterns()
        self.assertEqual(patterns, {})

    def test_no_timestamps(self):
        """Test with messages without timestamps."""
        messages = [
            {'sender': 'Alice', 'text': 'Hello', 'platform': 'test'},
            {'sender': 'Bob', 'text': 'Hi', 'platform': 'test'}
        ]
        analyzer = ConversationAnalyzer(messages)
        freq = analyzer.analyze_frequency_patterns()
        self.assertEqual(freq['total_messages'], 2)


if __name__ == '__main__':
    unittest.main()

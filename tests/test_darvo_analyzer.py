"""Tests for DARVO analyzer module."""

import unittest
from datetime import datetime
from darvo_analyzer import DARVOAnalyzer


class TestDARVOAnalyzer(unittest.TestCase):
    """Test DARVO tactics analysis functionality."""

    def setUp(self):
        """Set up test data."""
        self.messages_with_darvo = [
            {
                'timestamp': datetime(2024, 1, 1, 10, 0),
                'sender': 'Abuser',
                'text': 'I never said that. You are making things up.',
                'platform': 'test'
            },
            {
                'timestamp': datetime(2024, 1, 1, 10, 5),
                'sender': 'Abuser',
                'text': "You're crazy and nobody will believe you.",
                'platform': 'test'
            },
            {
                'timestamp': datetime(2024, 1, 1, 10, 10),
                'sender': 'Abuser',
                'text': "I'm the victim here. You're abusing me.",
                'platform': 'test'
            }
        ]
        
        self.messages_with_child_focused = [
            {
                'timestamp': datetime(2024, 1, 2, 10, 0),
                'sender': 'Abuser',
                'text': "The children are afraid of you.",
                'platform': 'test'
            },
            {
                'timestamp': datetime(2024, 1, 2, 10, 5),
                'sender': 'Abuser',
                'text': "You're an unfit parent. I'll get full custody.",
                'platform': 'test'
            }
        ]

    def test_initialization_with_messages(self):
        """Test analyzer initialization with messages."""
        analyzer = DARVOAnalyzer(messages=self.messages_with_darvo)
        self.assertEqual(len(analyzer.messages), 3)

    def test_initialization_with_text(self):
        """Test analyzer initialization with text."""
        text = "I never said that. You're crazy. I'm the victim here."
        analyzer = DARVOAnalyzer(text=text)
        self.assertEqual(analyzer.text, text)

    def test_detect_deny_patterns(self):
        """Test denial pattern detection."""
        analyzer = DARVOAnalyzer(messages=self.messages_with_darvo)
        results = analyzer.analyze_darvo_patterns()
        
        deny_patterns = results['deny_patterns']
        self.assertIn('outright_denial', deny_patterns)
        self.assertGreater(deny_patterns['outright_denial']['count'], 0)

    def test_detect_attack_patterns(self):
        """Test attack pattern detection."""
        analyzer = DARVOAnalyzer(messages=self.messages_with_darvo)
        results = analyzer.analyze_darvo_patterns()
        
        attack_patterns = results['attack_patterns']
        self.assertIn('credibility_attacks', attack_patterns)
        self.assertGreater(attack_patterns['credibility_attacks']['count'], 0)

    def test_detect_reverse_patterns(self):
        """Test reverse victim/offender pattern detection."""
        analyzer = DARVOAnalyzer(messages=self.messages_with_darvo)
        results = analyzer.analyze_darvo_patterns()
        
        reverse_patterns = results['reverse_patterns']
        self.assertIn('self_victimization', reverse_patterns)
        self.assertGreater(reverse_patterns['self_victimization']['count'], 0)

    def test_detect_child_focused_patterns(self):
        """Test child-focused DARVO pattern detection."""
        analyzer = DARVOAnalyzer(messages=self.messages_with_child_focused)
        results = analyzer.analyze_darvo_patterns()
        
        child_patterns = results['child_focused_patterns']
        self.assertGreater(child_patterns['custody_threats']['count'], 0)

    def test_full_darvo_pattern_detection(self):
        """Test detection of complete DARVO sequence."""
        analyzer = DARVOAnalyzer(messages=self.messages_with_darvo)
        results = analyzer.analyze_darvo_patterns()
        
        forensic = results['forensic_summary']
        # Should detect all three components
        self.assertTrue(forensic['darvo_components_present']['deny'])
        self.assertTrue(forensic['darvo_components_present']['attack'])
        self.assertTrue(forensic['darvo_components_present']['reverse'])
        self.assertTrue(forensic['full_darvo_pattern_detected'])

    def test_severity_calculation(self):
        """Test severity score calculation."""
        analyzer = DARVOAnalyzer(messages=self.messages_with_darvo)
        results = analyzer.analyze_darvo_patterns()
        
        severity = results['severity_assessment']
        self.assertIn('total_score', severity)
        self.assertIn('risk_level', severity)
        self.assertGreater(severity['total_score'], 0)
        self.assertIn(severity['risk_level'], ['low', 'medium', 'high', 'critical'])

    def test_child_focused_severity(self):
        """Test that child-focused patterns elevate severity."""
        analyzer = DARVOAnalyzer(messages=self.messages_with_child_focused)
        results = analyzer.analyze_darvo_patterns()
        
        severity = results['severity_assessment']
        forensic = results['forensic_summary']
        
        # Child-focused patterns should trigger high risk
        self.assertTrue(forensic['high_risk_indicators'])
        self.assertGreater(severity['category_scores']['child_focused'], 0)

    def test_compound_pattern_detection(self):
        """Test detection of compound DARVO sequences."""
        analyzer = DARVOAnalyzer(messages=self.messages_with_darvo)
        results = analyzer.analyze_darvo_patterns()
        
        compound = results['compound_patterns']
        # With deny, attack, reverse in sequence, should detect compound pattern
        self.assertIsInstance(compound, list)

    def test_forensic_summary_generation(self):
        """Test forensic summary generation."""
        analyzer = DARVOAnalyzer(messages=self.messages_with_darvo)
        results = analyzer.analyze_darvo_patterns()
        
        forensic = results['forensic_summary']
        self.assertIn('analysis_date', forensic)
        self.assertIn('total_messages_analyzed', forensic)
        self.assertIn('recommended_actions', forensic)
        self.assertIsInstance(forensic['recommended_actions'], list)

    def test_empty_messages(self):
        """Test with empty message list."""
        analyzer = DARVOAnalyzer(messages=[])
        results = analyzer.analyze_darvo_patterns()
        
        # Should return results without errors
        self.assertIn('deny_patterns', results)
        self.assertIn('attack_patterns', results)

    def test_messages_without_timestamps(self):
        """Test with messages without timestamps."""
        messages = [
            {'sender': 'A', 'text': 'I never said that', 'platform': 'test'},
            {'sender': 'A', 'text': "You're crazy", 'platform': 'test'}
        ]
        analyzer = DARVOAnalyzer(messages=messages)
        results = analyzer.analyze_darvo_patterns()
        
        # Should still analyze patterns
        self.assertIn('deny_patterns', results)
        self.assertIn('attack_patterns', results)

    def test_text_analysis(self):
        """Test document text analysis."""
        text = "I never said that. You're making things up. You're crazy and unstable. I'm the victim here. You're abusing me. Everyone will see the truth."
        analyzer = DARVOAnalyzer(text=text)
        results = analyzer.analyze_darvo_patterns()
        
        # Should detect DARVO components
        forensic = results['forensic_summary']
        self.assertTrue(forensic['darvo_components_present']['deny'])
        self.assertTrue(forensic['darvo_components_present']['attack'])
        self.assertTrue(forensic['darvo_components_present']['reverse'])

    def test_institutional_pattern_detection(self):
        """Test institutional/legal DARVO pattern detection."""
        messages = [
            {
                'timestamp': datetime(2024, 1, 3, 10, 0),
                'sender': 'Abuser',
                'text': 'She is making false allegations to the court.',
                'platform': 'test'
            },
            {
                'timestamp': datetime(2024, 1, 3, 10, 5),
                'sender': 'Abuser',
                'text': 'Parental alienation syndrome. She coached the children.',
                'platform': 'test'
            }
        ]
        analyzer = DARVOAnalyzer(messages=messages)
        results = analyzer.analyze_darvo_patterns()
        
        institutional = results['institutional_patterns']
        self.assertGreater(institutional['court_manipulation']['count'], 0)

    def test_timeline_analysis(self):
        """Test timeline analysis of DARVO patterns."""
        # Create messages over multiple weeks
        messages = []
        for i in range(15):
            messages.append({
                'timestamp': datetime(2024, 1, 1 + i, 10, 0),
                'sender': 'Abuser',
                'text': f"I never said that. You're crazy. I'm the victim. Day {i}",
                'platform': 'test'
            })
        
        analyzer = DARVOAnalyzer(messages=messages)
        results = analyzer.analyze_darvo_patterns()
        
        timeline = results['timeline_analysis']
        self.assertTrue(timeline['timeline_available'])
        self.assertIn('time_windows', timeline)

    def test_recommendations_generated(self):
        """Test that appropriate recommendations are generated."""
        # Full DARVO pattern should generate recommendations
        analyzer = DARVOAnalyzer(messages=self.messages_with_darvo)
        results = analyzer.analyze_darvo_patterns()
        
        forensic = results['forensic_summary']
        recommendations = forensic['recommended_actions']
        
        self.assertGreater(len(recommendations), 0)
        self.assertIsInstance(recommendations[0], str)

    def test_child_focused_recommendations(self):
        """Test that child-focused patterns generate urgent recommendations."""
        analyzer = DARVOAnalyzer(messages=self.messages_with_child_focused)
        results = analyzer.analyze_darvo_patterns()
        
        forensic = results['forensic_summary']
        recommendations = forensic['recommended_actions']
        
        # Should include urgent child-related recommendations
        urgent_found = any('URGENT' in r or 'child' in r.lower() for r in recommendations)
        self.assertTrue(urgent_found)


if __name__ == '__main__':
    unittest.main()

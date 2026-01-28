import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analyze import analyze_text, extract_text_from_pdf, normalize_text

class TestAbuseAnalysis(unittest.TestCase):

    def test_analyze_text_no_matches(self):
        text = "This is a normal document with no abuse indicators."
        results = analyze_text(text)
        self.assertEqual(results, {})

    def test_analyze_text_single_category(self):
        text = "He called me stupid and useless."
        results = analyze_text(text)
        self.assertIn("Emotional Abuse / Degradation", results)
        self.assertIn("stupid", results["Emotional Abuse / Degradation"])
        self.assertIn("useless", results["Emotional Abuse / Degradation"])

    def test_analyze_text_multiple_categories(self):
        text = "He said I can't spend my money and threatened to hit me."
        results = analyze_text(text)
        self.assertIn("Financial Control", results)
        self.assertIn("Threats / Intimidation", results)
        self.assertIn("my money", results["Financial Control"])
        self.assertIn("hit", results["Threats / Intimidation"])

    def test_case_insensitivity(self):
        text = "HE CALLED ME STUPID."
        results = analyze_text(text)
        self.assertIn("Emotional Abuse / Degradation", results)
        self.assertIn("stupid", results["Emotional Abuse / Degradation"])

    def test_false_positive_prevention(self):
        # "fat" should not match "father"
        text = "My father went to the store."
        results = analyze_text(text)
        # Assuming "father" is not a keyword, and "fat" is.
        # "fat" is in the indicators list.
        self.assertNotIn("Emotional Abuse / Degradation", results)

        # "hit" should not match "white"
        text = "The wall was painted white."
        results = analyze_text(text)
        self.assertNotIn("Threats / Intimidation", results)

    def test_smart_quotes(self):
        # "don't" uses a straight quote in keywords list
        # We test with a smart quote
        text = "He said don’t go out."
        results = analyze_text(text)
        self.assertIn("Isolation", results)
        self.assertIn("don't go out", results["Isolation"])

    @patch('analyze.PdfReader')
    def test_extract_text_from_pdf(self, mock_pdf_reader):
        # Setup mock
        mock_reader_instance = MagicMock()
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Mock extracted text."
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance

        # Test
        text = extract_text_from_pdf("dummy.pdf")
        self.assertEqual(text, "Mock extracted text.\n")

    @patch('analyze.PdfReader')
    def test_extract_text_failure(self, mock_pdf_reader):
        mock_pdf_reader.side_effect = Exception("File not found")

        text = extract_text_from_pdf("nonexistent.pdf")
        self.assertIsNone(text)

if __name__ == '__main__':
    unittest.main()

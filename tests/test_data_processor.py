"""Tests for data processor module."""

import unittest
import tempfile
import os
from pathlib import Path
from data_processor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    """Test data processing functionality."""

    def setUp(self):
        """Set up test files."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_detect_text_type(self):
        """Test file type detection for text files."""
        filepath = os.path.join(self.temp_dir, 'test.txt')
        with open(filepath, 'w') as f:
            f.write('Test content')

        processor = DataProcessor(filepath)
        self.assertEqual(processor.data_type, 'text')

    def test_detect_json_type(self):
        """Test file type detection for JSON files."""
        filepath = os.path.join(self.temp_dir, 'test.json')
        with open(filepath, 'w') as f:
            f.write('{}')

        processor = DataProcessor(filepath)
        self.assertEqual(processor.data_type, 'json')

    def test_file_not_found(self):
        """Test error handling for non-existent file."""
        with self.assertRaises(FileNotFoundError):
            DataProcessor('/nonexistent/file.txt')

    def test_get_text_content(self):
        """Test text content extraction."""
        filepath = os.path.join(self.temp_dir, 'test.txt')
        test_content = 'Test content for extraction'
        with open(filepath, 'w') as f:
            f.write(test_content)

        processor = DataProcessor(filepath)
        content = processor.get_text_content()
        self.assertEqual(content, test_content)


if __name__ == '__main__':
    unittest.main()

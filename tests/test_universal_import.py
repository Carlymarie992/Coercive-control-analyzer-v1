"""Tests for the universal import handler and new parsers."""

import unittest
import tempfile
import os
import json
from pathlib import Path

from universal_import_handler import UniversalImportHandler
from parsers.facebook_json_parser import FacebookJSONParser
from parsers.instagram_json_parser import InstagramJSONParser
from parsers.imessage_txt_parser import iMessageTxtParser
from parsers.imessage_csv_parser import iMessageCSVParser
from parsers.generic_regex_parser import GenericRegexParser
from file_upload_handler import FileUploadHandler


class TestUniversalImportHandler(unittest.TestCase):
    """Test universal import handler functionality."""

    def setUp(self):
        """Set up test environment."""
        self.handler = UniversalImportHandler()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_get_supported_platforms(self):
        """Test getting list of supported platforms."""
        platforms = self.handler.get_supported_platforms()
        self.assertIn('whatsapp', platforms)
        self.assertIn('facebook_json', platforms)
        self.assertIn('instagram', platforms)
        self.assertIn('imessage_txt', platforms)

    def test_get_supported_extensions(self):
        """Test getting list of supported extensions."""
        extensions = self.handler.get_supported_extensions()
        self.assertIn('.txt', extensions)
        self.assertIn('.json', extensions)
        self.assertIn('.eml', extensions)

    def test_is_platform_supported(self):
        """Test platform support checking."""
        self.assertTrue(self.handler.is_platform_supported('whatsapp'))
        self.assertTrue(self.handler.is_platform_supported('instagram'))
        self.assertFalse(self.handler.is_platform_supported('unknown'))

    def test_is_extension_supported(self):
        """Test extension support checking."""
        self.assertTrue(self.handler.is_extension_supported('.txt'))
        self.assertTrue(self.handler.is_extension_supported('json'))
        self.assertFalse(self.handler.is_extension_supported('.xyz'))


class TestFacebookJSONParser(unittest.TestCase):
    """Test Facebook JSON parser."""

    def setUp(self):
        """Set up test environment."""
        self.parser = FacebookJSONParser()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parse_facebook_json(self):
        """Test parsing Facebook JSON export."""
        # Create test Facebook JSON file
        test_data = {
            'participants': [{'name': 'User1'}, {'name': 'User2'}],
            'messages': [
                {
                    'sender_name': 'User1',
                    'timestamp_ms': 1609459200000,
                    'content': 'Hello'
                },
                {
                    'sender_name': 'User2',
                    'timestamp_ms': 1609459260000,
                    'content': 'Hi there'
                }
            ]
        }

        filepath = os.path.join(self.temp_dir, 'facebook.json')
        with open(filepath, 'w') as f:
            json.dump(test_data, f)

        messages = self.parser.parse_file(filepath)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['sender'], 'User1')
        self.assertEqual(messages[0]['text'], 'Hello')
        self.assertEqual(messages[0]['platform'], 'facebook')


class TestInstagramJSONParser(unittest.TestCase):
    """Test Instagram JSON parser."""

    def setUp(self):
        """Set up test environment."""
        self.parser = InstagramJSONParser()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parse_instagram_json(self):
        """Test parsing Instagram JSON export."""
        # Create test Instagram JSON file
        test_data = {
            'participants': [{'name': 'user1'}, {'name': 'user2'}],
            'messages': [
                {
                    'sender_name': 'user1',
                    'timestamp_ms': 1609459200000,
                    'content': 'Hey!'
                },
                {
                    'sender_name': 'user2',
                    'timestamp_ms': 1609459260000,
                    'content': 'Hello!'
                }
            ]
        }

        filepath = os.path.join(self.temp_dir, 'instagram.json')
        with open(filepath, 'w') as f:
            json.dump(test_data, f)

        messages = self.parser.parse_file(filepath)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['sender'], 'user1')
        self.assertEqual(messages[0]['platform'], 'instagram')


class TestiMessageTxtParser(unittest.TestCase):
    """Test iMessage text parser."""

    def setUp(self):
        """Set up test environment."""
        self.parser = iMessageTxtParser()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parse_imessage_txt(self):
        """Test parsing iMessage text export."""
        # Create test iMessage text file
        test_content = """[2024-01-01 10:00:00] Alice: Hello!
[2024-01-01 10:01:00] Bob: Hi Alice!
[2024-01-01 10:02:00] Alice: How are you?
"""
        filepath = os.path.join(self.temp_dir, 'imessage.txt')
        with open(filepath, 'w') as f:
            f.write(test_content)

        messages = self.parser.parse_file(filepath)
        self.assertEqual(len(messages), 3)
        self.assertEqual(messages[0]['sender'], 'Alice')
        self.assertEqual(messages[0]['text'], 'Hello!')
        self.assertEqual(messages[0]['platform'], 'imessage')


class TestiMessageCSVParser(unittest.TestCase):
    """Test iMessage CSV parser."""

    def setUp(self):
        """Set up test environment."""
        self.parser = iMessageCSVParser()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parse_imessage_csv(self):
        """Test parsing iMessage CSV export."""
        # Create test iMessage CSV file
        test_content = """timestamp,sender,message,is_from_me
2024-01-01 10:00:00,Alice,Hello!,0
2024-01-01 10:01:00,Bob,Hi Alice!,1
"""
        filepath = os.path.join(self.temp_dir, 'imessage.csv')
        with open(filepath, 'w') as f:
            f.write(test_content)

        messages = self.parser.parse_file(filepath)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['sender'], 'Alice')
        self.assertEqual(messages[1]['sender'], 'Me')
        self.assertEqual(messages[0]['platform'], 'imessage')


class TestGenericRegexParser(unittest.TestCase):
    """Test generic regex parser."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parse_with_template(self):
        """Test parsing with predefined template."""
        # Create test file
        test_content = """2024-01-01 10:00:00 - Alice: Hello!
2024-01-01 10:01:00 - Bob: Hi there!
"""
        filepath = os.path.join(self.temp_dir, 'test.txt')
        with open(filepath, 'w') as f:
            f.write(test_content)

        parser = GenericRegexParser(template='basic_timestamp')
        messages = parser.parse_file(filepath)
        
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['sender'], 'Alice')
        self.assertEqual(messages[0]['text'], 'Hello!')

    def test_get_available_templates(self):
        """Test getting available templates."""
        templates = GenericRegexParser.get_available_templates()
        self.assertIn('basic_timestamp', templates)
        self.assertIn('bracketed_timestamp', templates)


class TestFileUploadHandler(unittest.TestCase):
    """Test file upload handler."""

    def setUp(self):
        """Set up test environment."""
        self.handler = FileUploadHandler()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_validate_file_success(self):
        """Test successful file validation."""
        filepath = os.path.join(self.temp_dir, 'test.txt')
        with open(filepath, 'w') as f:
            f.write('Test content')

        is_valid, error = self.handler.validate_file(filepath)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_file_not_found(self):
        """Test validation of non-existent file."""
        is_valid, error = self.handler.validate_file('/nonexistent/file.txt')
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

    def test_validate_file_empty(self):
        """Test validation of empty file."""
        filepath = os.path.join(self.temp_dir, 'empty.txt')
        Path(filepath).touch()

        is_valid, error = self.handler.validate_file(filepath)
        self.assertFalse(is_valid)
        self.assertIn('empty', error.lower())

    def test_get_supported_platforms(self):
        """Test getting supported platforms."""
        platforms = self.handler.get_supported_platforms()
        self.assertGreater(len(platforms), 0)
        self.assertTrue(any(p['id'] == 'whatsapp' for p in platforms))


if __name__ == '__main__':
    unittest.main()

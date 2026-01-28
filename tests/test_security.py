"""Tests for security modules."""

import unittest
import tempfile
import os
from pathlib import Path
from security.anonymization import DataAnonymizer
from security.encryption import DataEncryptor, generate_new_key


class TestDataAnonymizer(unittest.TestCase):
    """Test data anonymization functionality."""

    def setUp(self):
        """Set up anonymizer."""
        self.anonymizer = DataAnonymizer()

    def test_anonymize_email(self):
        """Test email anonymization."""
        text = "Contact me at john.doe@example.com"
        result = self.anonymizer.anonymize_text(text)

        self.assertNotIn('john.doe@example.com', result)
        self.assertIn('[EMAIL-', result)

    def test_anonymize_phone(self):
        """Test phone number anonymization."""
        text = "Call me at 555-123-4567"
        result = self.anonymizer.anonymize_text(text)

        self.assertNotIn('555-123-4567', result)
        self.assertIn('[PHONE-', result)

    def test_anonymize_conversation(self):
        """Test conversation anonymization."""
        messages = [
            {'sender': 'John', 'text': 'My email is john@test.com'},
            {'sender': 'Jane', 'text': 'Call 555-1234'}
        ]

        result = self.anonymizer.anonymize_conversation(messages)

        # Senders should be anonymized
        self.assertNotEqual(result[0]['sender'], 'John')
        self.assertNotEqual(result[1]['sender'], 'Jane')

        # Email should be anonymized
        self.assertNotIn('john@test.com', result[0]['text'])

    def test_consistent_replacements(self):
        """Test that same values get same replacements."""
        text1 = "Email: test@example.com"
        text2 = "Contact: test@example.com"

        result1 = self.anonymizer.anonymize_text(text1)
        result2 = self.anonymizer.anonymize_text(text2)

        # Extract the replacement
        import re
        match1 = re.search(r'\[EMAIL-([^\]]+)\]', result1)
        match2 = re.search(r'\[EMAIL-([^\]]+)\]', result2)

        self.assertEqual(match1.group(1), match2.group(1))


class TestDataEncryptor(unittest.TestCase):
    """Test data encryption functionality."""

    def setUp(self):
        """Set up encryptor."""
        self.key = generate_new_key()
        self.encryptor = DataEncryptor(self.key)
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_encrypt_decrypt_text(self):
        """Test text encryption and decryption."""
        original = "Sensitive information"
        encrypted = self.encryptor.encrypt_text(original)
        decrypted = self.encryptor.decrypt_text(encrypted)

        self.assertNotEqual(original, encrypted)
        self.assertEqual(original, decrypted)

    def test_encrypt_decrypt_file(self):
        """Test file encryption and decryption."""
        # Create test file
        original_path = os.path.join(self.temp_dir, 'test.txt')
        with open(original_path, 'w') as f:
            f.write('Secret content')

        # Encrypt
        encrypted_path = self.encryptor.encrypt_file(original_path)
        self.assertTrue(os.path.exists(encrypted_path))

        # Verify encrypted content is different
        with open(encrypted_path, 'rb') as f:
            encrypted_content = f.read()
        with open(original_path, 'rb') as f:
            original_content = f.read()
        self.assertNotEqual(encrypted_content, original_content)

        # Decrypt
        decrypted_path = self.encryptor.decrypt_file(encrypted_path)
        with open(decrypted_path, 'r') as f:
            decrypted_content = f.read()

        self.assertEqual(decrypted_content, 'Secret content')

    def test_key_from_password(self):
        """Test key generation from password."""
        password = "test_password_123"
        key1, salt = DataEncryptor.generate_key_from_password(password)
        key2, _ = DataEncryptor.generate_key_from_password(password, salt)

        # Same password and salt should generate same key
        self.assertEqual(key1, key2)


if __name__ == '__main__':
    unittest.main()

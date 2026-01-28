"""Security configurations for handling sensitive data."""

import os
from cryptography.fernet import Fernet

# Encryption settings
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')  # Should be set in environment
DEFAULT_KEY_SIZE = 32  # bytes for AES-256

# Data retention settings
SECURE_DELETE_PASSES = int(os.getenv('SECURE_DELETE_PASSES', '3'))
AUTO_DELETE_TEMP_FILES = os.getenv('AUTO_DELETE_TEMP_FILES', 'True').lower() == 'true'

# Anonymization settings
ANONYMIZE_NAMES = os.getenv('ANONYMIZE_NAMES', 'True').lower() == 'true'
ANONYMIZE_LOCATIONS = os.getenv('ANONYMIZE_LOCATIONS', 'True').lower() == 'true'
ANONYMIZE_PHONE_NUMBERS = os.getenv('ANONYMIZE_PHONE_NUMBERS', 'True').lower() == 'true'
ANONYMIZE_EMAILS = os.getenv('ANONYMIZE_EMAILS', 'True').lower() == 'true'

# File security settings
SECURE_FILE_PERMISSIONS = 0o600  # Owner read/write only
SECURE_DIR_PERMISSIONS = 0o700   # Owner read/write/execute only

# Password/Key requirements
MIN_PASSWORD_LENGTH = int(os.getenv('MIN_PASSWORD_LENGTH', '12'))
REQUIRE_STRONG_PASSWORDS = os.getenv('REQUIRE_STRONG_PASSWORDS', 'True').lower() == 'true'

# Session settings
SESSION_TIMEOUT_MINUTES = int(os.getenv('SESSION_TIMEOUT_MINUTES', '30'))
MAX_LOGIN_ATTEMPTS = int(os.getenv('MAX_LOGIN_ATTEMPTS', '3'))

# Privacy settings
COLLECT_ANALYTICS = os.getenv('COLLECT_ANALYTICS', 'False').lower() == 'true'
SHARE_ANONYMOUS_STATS = os.getenv('SHARE_ANONYMOUS_STATS', 'False').lower() == 'true'


def generate_encryption_key():
    """Generate a new encryption key for Fernet."""
    return Fernet.generate_key()


def get_encryption_key():
    """Get or generate encryption key."""
    if ENCRYPTION_KEY:
        return ENCRYPTION_KEY.encode()
    # Generate a key if none exists (not recommended for production)
    return generate_encryption_key()

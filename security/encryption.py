"""Data encryption for sensitive information."""

import os
from pathlib import Path
from typing import Union, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64

from config.security import get_encryption_key, SECURE_FILE_PERMISSIONS


class DataEncryptor:
    """Handle encryption and decryption of sensitive data."""

    def __init__(self, key: Optional[bytes] = None):
        """
        Initialize encryptor.

        Args:
            key: Encryption key. If None, uses key from config.
        """
        if key is None:
            key = get_encryption_key()
        self.cipher = Fernet(key)

    @staticmethod
    def generate_key_from_password(password: str, salt: Optional[bytes] = None) -> tuple:
        """
        Generate encryption key from password.

        Args:
            password: Password string
            salt: Salt bytes. If None, generates new salt.

        Returns:
            Tuple of (key, salt)
        """
        if salt is None:
            salt = os.urandom(16)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    def encrypt_text(self, text: str) -> bytes:
        """
        Encrypt text string.

        Args:
            text: Text to encrypt

        Returns:
            Encrypted bytes
        """
        return self.cipher.encrypt(text.encode('utf-8'))

    def decrypt_text(self, encrypted_data: bytes) -> str:
        """
        Decrypt encrypted data.

        Args:
            encrypted_data: Encrypted bytes

        Returns:
            Decrypted text
        """
        return self.cipher.decrypt(encrypted_data).decode('utf-8')

    def encrypt_file(self, filepath: Union[str, Path], output_path: Optional[Union[str, Path]] = None):
        """
        Encrypt a file.

        Args:
            filepath: Path to file to encrypt
            output_path: Path for encrypted file. If None, overwrites original.
        """
        filepath = Path(filepath)

        # Read file
        with open(filepath, 'rb') as f:
            data = f.read()

        # Encrypt
        encrypted_data = self.cipher.encrypt(data)

        # Write encrypted file
        output_path = Path(output_path) if output_path else filepath.with_suffix(filepath.suffix + '.enc')
        with open(output_path, 'wb') as f:
            f.write(encrypted_data)

        # Set secure permissions
        os.chmod(output_path, SECURE_FILE_PERMISSIONS)

        return str(output_path)

    def decrypt_file(self, filepath: Union[str, Path], output_path: Optional[Union[str, Path]] = None):
        """
        Decrypt a file.

        Args:
            filepath: Path to encrypted file
            output_path: Path for decrypted file. If None, removes .enc extension.
        """
        filepath = Path(filepath)

        # Read encrypted file
        with open(filepath, 'rb') as f:
            encrypted_data = f.read()

        # Decrypt
        decrypted_data = self.cipher.decrypt(encrypted_data)

        # Write decrypted file
        if output_path is None:
            if filepath.suffix == '.enc':
                output_path = filepath.with_suffix('')
            else:
                output_path = filepath.with_suffix('.dec')
        else:
            output_path = Path(output_path)

        with open(output_path, 'wb') as f:
            f.write(decrypted_data)

        # Set secure permissions
        os.chmod(output_path, SECURE_FILE_PERMISSIONS)

        return str(output_path)

    def encrypt_dict(self, data: dict) -> dict:
        """
        Encrypt sensitive fields in a dictionary.

        Args:
            data: Dictionary to encrypt

        Returns:
            Dictionary with encrypted sensitive fields
        """
        import json

        # Convert to JSON and encrypt
        json_str = json.dumps(data)
        encrypted = self.encrypt_text(json_str)

        return {
            'encrypted': True,
            'data': base64.b64encode(encrypted).decode('utf-8')
        }

    def decrypt_dict(self, encrypted_data: dict) -> dict:
        """
        Decrypt dictionary.

        Args:
            encrypted_data: Encrypted dictionary

        Returns:
            Decrypted dictionary
        """
        import json

        if not encrypted_data.get('encrypted'):
            return encrypted_data

        encrypted_bytes = base64.b64decode(encrypted_data['data'])
        decrypted_str = self.decrypt_text(encrypted_bytes)

        return json.loads(decrypted_str)


def generate_new_key() -> bytes:
    """Generate a new encryption key."""
    return Fernet.generate_key()


def save_key_to_file(key: bytes, filepath: Union[str, Path]):
    """
    Save encryption key to file securely.

    Args:
        key: Encryption key
        filepath: Path to save key
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'wb') as f:
        f.write(key)

    # Set secure permissions (owner read/write only)
    os.chmod(filepath, SECURE_FILE_PERMISSIONS)


def load_key_from_file(filepath: Union[str, Path]) -> bytes:
    """
    Load encryption key from file.

    Args:
        filepath: Path to key file

    Returns:
        Encryption key
    """
    with open(filepath, 'rb') as f:
        return f.read()

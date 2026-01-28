"""Secure storage utilities for sensitive data."""

import os
import shutil
from pathlib import Path
from typing import Union, Optional
import tempfile

from config.security import (
    SECURE_FILE_PERMISSIONS,
    SECURE_DIR_PERMISSIONS,
    AUTO_DELETE_TEMP_FILES,
    SECURE_DELETE_PASSES
)
from security.encryption import DataEncryptor


class SecureStorage:
    """Handle secure storage and deletion of sensitive files."""

    def __init__(self, base_dir: Optional[Union[str, Path]] = None):
        """
        Initialize secure storage.

        Args:
            base_dir: Base directory for secure storage
        """
        if base_dir:
            self.base_dir = Path(base_dir)
            self.base_dir.mkdir(parents=True, exist_ok=True)
            os.chmod(self.base_dir, SECURE_DIR_PERMISSIONS)
        else:
            self.base_dir = None

        self.temp_files = []

    def create_secure_file(self, filename: str, content: Union[str, bytes],
                           encrypt: bool = False) -> Path:
        """
        Create a file with secure permissions.

        Args:
            filename: Name of file
            content: Content to write
            encrypt: Whether to encrypt the content

        Returns:
            Path to created file
        """
        if self.base_dir:
            filepath = self.base_dir / filename
        else:
            filepath = Path(filename)

        # Ensure parent directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Encrypt if requested
        if encrypt:
            encryptor = DataEncryptor()
            if isinstance(content, str):
                content = encryptor.encrypt_text(content)
            else:
                content = encryptor.cipher.encrypt(content)

        # Write content
        mode = 'wb' if isinstance(content, bytes) else 'w'
        with open(filepath, mode) as f:
            f.write(content)

        # Set secure permissions
        os.chmod(filepath, SECURE_FILE_PERMISSIONS)

        return filepath

    def create_temp_file(self, content: Union[str, bytes],
                         suffix: str = '', prefix: str = 'tmp',
                         encrypt: bool = False) -> Path:
        """
        Create a temporary file with secure permissions.

        Args:
            content: Content to write
            suffix: File suffix
            prefix: File prefix
            encrypt: Whether to encrypt the content

        Returns:
            Path to temp file
        """
        # Create temp file
        fd, temp_path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
        temp_path = Path(temp_path)

        try:
            # Encrypt if requested
            if encrypt:
                encryptor = DataEncryptor()
                if isinstance(content, str):
                    content = encryptor.encrypt_text(content)
                else:
                    content = encryptor.cipher.encrypt(content)

            # Write content
            if isinstance(content, bytes):
                os.write(fd, content)
            else:
                os.write(fd, content.encode('utf-8'))

            # Set secure permissions
            os.chmod(temp_path, SECURE_FILE_PERMISSIONS)

            # Track for cleanup
            self.temp_files.append(temp_path)

            return temp_path

        finally:
            os.close(fd)

    def secure_delete(self, filepath: Union[str, Path], passes: int = None):
        """
        Securely delete a file by overwriting before deletion.

        Args:
            filepath: Path to file to delete
            passes: Number of overwrite passes (default from config)
        """
        filepath = Path(filepath)
        if not filepath.exists():
            return

        passes = passes or SECURE_DELETE_PASSES

        # Get file size
        file_size = filepath.stat().st_size

        # Overwrite file multiple times
        for _ in range(passes):
            with open(filepath, 'wb') as f:
                # Write random data
                f.write(os.urandom(file_size))

        # Delete file
        filepath.unlink()

    def cleanup_temp_files(self):
        """Clean up all temporary files."""
        for temp_file in self.temp_files:
            try:
                if temp_file.exists():
                    self.secure_delete(temp_file)
            except Exception:
                # Best effort cleanup
                pass

        self.temp_files.clear()

    def create_secure_directory(self, dirname: str) -> Path:
        """
        Create directory with secure permissions.

        Args:
            dirname: Directory name

        Returns:
            Path to created directory
        """
        if self.base_dir:
            dirpath = self.base_dir / dirname
        else:
            dirpath = Path(dirname)

        dirpath.mkdir(parents=True, exist_ok=True)
        os.chmod(dirpath, SECURE_DIR_PERMISSIONS)

        return dirpath

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup temp files."""
        if AUTO_DELETE_TEMP_FILES:
            self.cleanup_temp_files()


def secure_move(src: Union[str, Path], dst: Union[str, Path]):
    """
    Securely move a file (copy then secure delete).

    Args:
        src: Source path
        dst: Destination path
    """
    src = Path(src)
    dst = Path(dst)

    # Copy file
    shutil.copy2(src, dst)

    # Set secure permissions on destination
    os.chmod(dst, SECURE_FILE_PERMISSIONS)

    # Secure delete source
    storage = SecureStorage()
    storage.secure_delete(src)


def secure_copy(src: Union[str, Path], dst: Union[str, Path]):
    """
    Securely copy a file with secure permissions.

    Args:
        src: Source path
        dst: Destination path
    """
    dst = Path(dst)
    shutil.copy2(src, dst)
    os.chmod(dst, SECURE_FILE_PERMISSIONS)

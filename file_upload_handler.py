"""Universal file upload handler with platform detection and validation."""

import os
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from universal_import_handler import UniversalImportHandler


class FileUploadHandler:
    """
    Universal file upload handler with comprehensive format support.
    Provides platform detection, validation, and error handling.
    """

    # Maximum file size in MB
    MAX_FILE_SIZE_MB = 100

    # Supported file extensions
    SUPPORTED_EXTENSIONS = [
        '.txt', '.csv', '.json', '.xml', '.html', '.htm',
        '.eml', '.mbox', '.pdf', '.docx', '.log', '.chat'
    ]

    def __init__(self):
        """Initialize the file upload handler."""
        self.import_handler = UniversalImportHandler()
        self.last_error = None
        self.last_warning = None

    def validate_file(self, filepath: str) -> Tuple[bool, Optional[str]]:
        """
        Validate an uploaded file.

        Args:
            filepath: Path to the file

        Returns:
            Tuple of (is_valid, error_message)
        """
        filepath = Path(filepath)

        # Check if file exists
        if not filepath.exists():
            return False, f"File not found: {filepath}"

        # Check if it's a file (not directory)
        if not filepath.is_file():
            return False, f"Path is not a file: {filepath}"

        # Check file size
        file_size_mb = filepath.stat().st_size / (1024 * 1024)
        if file_size_mb > self.MAX_FILE_SIZE_MB:
            return False, f"File size ({file_size_mb:.2f} MB) exceeds maximum allowed size ({self.MAX_FILE_SIZE_MB} MB)"

        # Check if file is empty
        if filepath.stat().st_size == 0:
            return False, "File is empty"

        # Check file extension
        extension = filepath.suffix.lower()
        if extension not in self.SUPPORTED_EXTENSIONS:
            return False, f"Unsupported file extension: {extension}. Supported: {', '.join(self.SUPPORTED_EXTENSIONS)}"

        return True, None

    def detect_platform(self, filepath: str) -> Dict:
        """
        Detect platform from file with confidence score.

        Args:
            filepath: Path to the file

        Returns:
            Dictionary with detection results
        """
        # Validate file first
        is_valid, error = self.validate_file(filepath)
        if not is_valid:
            return {
                'success': False,
                'error': error,
                'platform': None,
                'confidence': 0.0
            }

        try:
            # Auto-detect platform
            platform = self.import_handler.detect_platform(filepath)

            # Determine confidence based on file characteristics
            confidence = self._calculate_confidence(filepath, platform)

            return {
                'success': True,
                'platform': platform,
                'confidence': confidence,
                'extension': Path(filepath).suffix.lower()
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'platform': None,
                'confidence': 0.0
            }

    def _calculate_confidence(self, filepath: str, platform: str) -> float:
        """Calculate confidence score for platform detection."""
        filepath = Path(filepath)
        extension = filepath.suffix.lower()

        # High confidence for specific extensions
        high_confidence_map = {
            '.xml': ['sms'],
            '.eml': ['email'],
            '.mbox': ['mbox'],
            '.html': ['facebook_html'],
            '.htm': ['facebook_html'],
        }

        if extension in high_confidence_map:
            if platform in high_confidence_map[extension]:
                return 0.95

        # Medium confidence for JSON (needs content analysis)
        if extension == '.json':
            return 0.75

        # Medium-low confidence for text files (ambiguous)
        if extension == '.txt':
            return 0.60

        # Medium confidence for CSV
        if extension == '.csv':
            return 0.70

        # Default confidence
        return 0.50

    def process_upload(self, filepath: str, platform: Optional[str] = None) -> Dict:
        """
        Process an uploaded file.

        Args:
            filepath: Path to the uploaded file
            platform: Optional platform override (auto-detected if None)

        Returns:
            Dictionary with processing results
        """
        # Validate file
        is_valid, error = self.validate_file(filepath)
        if not is_valid:
            return {
                'success': False,
                'error': error,
                'messages': [],
                'platform': None
            }

        try:
            # Parse the file
            messages = self.import_handler.parse_file(filepath, platform)

            # Auto-detect platform if not provided
            if platform is None:
                platform = self.import_handler.detect_platform(filepath)

            return {
                'success': True,
                'messages': messages,
                'message_count': len(messages),
                'platform': platform,
                'filepath': str(filepath)
            }

        except Exception as e:
            return {
                'success': False,
                'error': f"Error processing file: {str(e)}",
                'messages': [],
                'platform': platform
            }

    def get_supported_platforms(self) -> List[Dict]:
        """
        Get list of supported platforms with descriptions.

        Returns:
            List of platform info dictionaries
        """
        platforms = [
            {
                'id': 'whatsapp',
                'name': 'WhatsApp',
                'description': 'WhatsApp chat export (.txt)',
                'extensions': ['.txt']
            },
            {
                'id': 'sms',
                'name': 'SMS',
                'description': 'SMS backup (XML or CSV)',
                'extensions': ['.xml', '.csv']
            },
            {
                'id': 'discord',
                'name': 'Discord',
                'description': 'Discord chat export (.json)',
                'extensions': ['.json']
            },
            {
                'id': 'telegram',
                'name': 'Telegram',
                'description': 'Telegram chat export (.json)',
                'extensions': ['.json']
            },
            {
                'id': 'facebook_json',
                'name': 'Facebook Messenger (JSON)',
                'description': 'Facebook Messenger JSON export',
                'extensions': ['.json']
            },
            {
                'id': 'facebook_html',
                'name': 'Facebook Messenger (HTML)',
                'description': 'Facebook Messenger HTML export',
                'extensions': ['.html', '.htm']
            },
            {
                'id': 'instagram',
                'name': 'Instagram',
                'description': 'Instagram Direct Messages (.json)',
                'extensions': ['.json']
            },
            {
                'id': 'imessage_txt',
                'name': 'iMessage (Text)',
                'description': 'iMessage text export',
                'extensions': ['.txt']
            },
            {
                'id': 'imessage_csv',
                'name': 'iMessage (CSV)',
                'description': 'iMessage CSV export',
                'extensions': ['.csv']
            },
            {
                'id': 'email',
                'name': 'Email',
                'description': 'Email messages (.eml)',
                'extensions': ['.eml']
            },
            {
                'id': 'mbox',
                'name': 'MBOX',
                'description': 'Email archive (.mbox)',
                'extensions': ['.mbox']
            },
            {
                'id': 'generic',
                'name': 'Generic Text',
                'description': 'Generic text format',
                'extensions': ['.txt', '.log', '.chat']
            },
        ]
        return platforms

    def get_platform_by_id(self, platform_id: str) -> Optional[Dict]:
        """Get platform info by ID."""
        platforms = self.get_supported_platforms()
        for platform in platforms:
            if platform['id'] == platform_id:
                return platform
        return None

    def generate_error_message(self, error_type: str, **kwargs) -> str:
        """
        Generate user-friendly error messages.

        Args:
            error_type: Type of error
            **kwargs: Additional context for error message

        Returns:
            Formatted error message
        """
        max_size_mb = self.MAX_FILE_SIZE_MB
        supported_exts = ', '.join(self.SUPPORTED_EXTENSIONS)
        
        error_messages = {
            'file_not_found': "The file could not be found. Please check the file path and try again.",
            'file_too_large': f"The file is too large. Maximum file size is {max_size_mb} MB. Please split the file or compress it.",
            'file_empty': "The file is empty. Please upload a file with content.",
            'unsupported_format': f"This file format is not supported. Supported formats: {supported_exts}",
            'parse_error': "The file could not be parsed. Please check the file format and try selecting a different platform.",
            'unknown_platform': "The platform could not be detected automatically. Please select a platform manually.",
            'invalid_content': "The file content does not match the expected format for this platform.",
        }

        message = error_messages.get(error_type, "An unknown error occurred.")
        
        # Add context if provided
        if 'details' in kwargs:
            message += f"\n\nDetails: {kwargs['details']}"

        return message

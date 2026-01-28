"""Universal message import system with centralized parser registry."""

import os
import json
from pathlib import Path
from typing import Optional, List, Dict
import re


class UniversalImportHandler:
    """
    Centralized handler for importing messages from any platform.
    Provides auto-detection and unified interface for all parsers.
    """

    # Centralized parser registry mapping platforms to parser classes
    PARSER_MAP = {
        'whatsapp': 'parsers.whatsapp_parser.WhatsAppParser',
        'sms': 'parsers.sms_parser.SMSParser',
        'discord': 'parsers.discord_parser.DiscordParser',
        'telegram': 'parsers.telegram_parser.TelegramParser',
        'generic': 'parsers.generic_text_parser.GenericTextParser',
        'facebook_html': 'parsers.facebook_html_parser.FacebookHTMLParser',
        'facebook_json': 'parsers.facebook_json_parser.FacebookJSONParser',
        'instagram': 'parsers.instagram_json_parser.InstagramJSONParser',
        'imessage_txt': 'parsers.imessage_txt_parser.iMessageTxtParser',
        'imessage_csv': 'parsers.imessage_csv_parser.iMessageCSVParser',
        'email': 'parsers.email_parser.EmailParser',
        'mbox': 'parsers.mbox_parser.MboxParser',
        'generic_regex': 'parsers.generic_regex_parser.GenericRegexParser',
    }

    # File extension to platform mappings
    EXTENSION_MAP = {
        '.txt': ['whatsapp', 'generic', 'imessage_txt'],
        '.csv': ['sms', 'imessage_csv'],
        '.json': ['discord', 'telegram', 'facebook_json', 'instagram'],
        '.xml': ['sms'],
        '.html': ['facebook_html'],
        '.htm': ['facebook_html'],
        '.eml': ['email'],
        '.mbox': ['mbox'],
    }

    def __init__(self):
        """Initialize the universal import handler."""
        self._parser_cache = {}

    def detect_platform(self, filepath: str) -> str:
        """
        Auto-detect the platform from file characteristics.

        Args:
            filepath: Path to the conversation file

        Returns:
            Detected platform name
        """
        filepath = Path(filepath)
        extension = filepath.suffix.lower()

        # Check file extension first
        if extension not in self.EXTENSION_MAP:
            return 'generic'

        possible_platforms = self.EXTENSION_MAP[extension]

        # If only one possibility, return it
        if len(possible_platforms) == 1:
            return possible_platforms[0]

        # For JSON files, perform content analysis
        if extension == '.json':
            return self._detect_json_platform(filepath)

        # For text files, analyze content
        if extension == '.txt':
            return self._detect_text_platform(filepath)

        # For CSV files, check headers
        if extension == '.csv':
            return self._detect_csv_platform(filepath)

        # Default to first option
        return possible_platforms[0]

    def _detect_json_platform(self, filepath: Path) -> str:
        """Detect platform from JSON file structure."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                # Read first few KB to detect structure
                content = f.read(10000)
                data = json.loads(content)

            # Instagram: has 'participants' and specific structure
            if isinstance(data, dict):
                if 'participants' in data and 'messages' in data:
                    # Check for Instagram-specific fields
                    messages = data.get('messages', [])
                    if messages and isinstance(messages[0], dict):
                        if 'sender_name' in messages[0]:
                            return 'instagram'

                # Facebook: different structure than Instagram
                if 'messages' in data and 'participants' in data:
                    messages = data.get('messages', [])
                    if messages and isinstance(messages[0], dict):
                        if 'sender_name' in messages[0] and 'timestamp_ms' in messages[0]:
                            return 'facebook_json'

                # Telegram: has 'type' and 'id' fields at root
                if 'type' in data and data.get('type') == 'personal_chat':
                    return 'telegram'

                # Telegram: has messages array with 'from' field
                if 'messages' in data and isinstance(data['messages'], list):
                    if data['messages'] and 'from' in data['messages'][0]:
                        return 'telegram'

                # Discord: has different structure
                if 'messages' in data or 'channel' in data:
                    return 'discord'

            # List format - likely Discord
            if isinstance(data, list):
                if data and isinstance(data[0], dict):
                    if 'author' in data[0] or 'content' in data[0]:
                        return 'discord'

        except (json.JSONDecodeError, FileNotFoundError, KeyError):
            pass

        # Default to Discord for JSON
        return 'discord'

    def _detect_text_platform(self, filepath: Path) -> str:
        """Detect platform from text file patterns."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                # Read first 20 lines for pattern detection
                lines = [f.readline() for _ in range(20)]
                content = ''.join(lines)

            # WhatsApp patterns
            # Format: [DD/MM/YYYY, HH:MM:SS] or DD/MM/YYYY, HH:MM - Sender: Message
            whatsapp_pattern = r'\[?\d{1,2}/\d{1,2}/\d{2,4},?\s+\d{1,2}:\d{2}'
            if re.search(whatsapp_pattern, content):
                return 'whatsapp'

            # iMessage patterns (often have clean timestamp lines)
            # Format: [YYYY-MM-DD HH:MM:SS] or similar structured format
            imessage_pattern = r'\[\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\]'
            if re.search(imessage_pattern, content):
                return 'imessage_txt'

        except (FileNotFoundError, UnicodeDecodeError):
            pass

        # Default to generic for text files
        return 'generic'

    def _detect_csv_platform(self, filepath: Path) -> str:
        """Detect platform from CSV headers."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                first_line = f.readline().lower()

            # iMessage CSV typically has specific headers
            if 'imessage' in first_line or 'is_from_me' in first_line:
                return 'imessage_csv'

            # SMS CSV headers
            if 'address' in first_line or 'type' in first_line or 'date' in first_line:
                return 'sms'

        except (FileNotFoundError, UnicodeDecodeError):
            pass

        # Default to SMS for CSV
        return 'sms'

    def get_parser(self, platform: str):
        """
        Get parser instance for a platform.

        Args:
            platform: Platform name

        Returns:
            Parser instance

        Raises:
            ValueError: If platform is not supported
        """
        if platform not in self.PARSER_MAP:
            raise ValueError(f"Unsupported platform: {platform}")

        # Use cached parser if available
        if platform in self._parser_cache:
            return self._parser_cache[platform]

        # Import and instantiate parser
        parser_path = self.PARSER_MAP[platform]
        module_path, class_name = parser_path.rsplit('.', 1)

        try:
            # Dynamic import
            import importlib
            module = importlib.import_module(module_path)
            parser_class = getattr(module, class_name)
            parser = parser_class()

            # Cache the parser
            self._parser_cache[platform] = parser
            return parser

        except (ImportError, AttributeError) as e:
            raise ValueError(f"Failed to load parser for {platform}: {e}")

    def parse_file(self, filepath: str, platform: Optional[str] = None) -> List[Dict]:
        """
        Parse a conversation file with auto-detection.

        Args:
            filepath: Path to the conversation file
            platform: Platform type (auto-detected if None)

        Returns:
            List of message dictionaries

        Raises:
            ValueError: If file cannot be parsed
        """
        # Auto-detect platform if not specified
        if platform is None:
            platform = self.detect_platform(filepath)

        # Get appropriate parser
        parser = self.get_parser(platform)

        # Parse the file
        try:
            messages = parser.parse_file(filepath)
            return messages
        except Exception as e:
            raise ValueError(f"Error parsing file as {platform}: {e}")

    def get_supported_platforms(self) -> List[str]:
        """
        Get list of all supported platforms.

        Returns:
            List of platform names
        """
        return list(self.PARSER_MAP.keys())

    def get_supported_extensions(self) -> List[str]:
        """
        Get list of all supported file extensions.

        Returns:
            List of file extensions
        """
        return list(self.EXTENSION_MAP.keys())

    def is_platform_supported(self, platform: str) -> bool:
        """
        Check if a platform is supported.

        Args:
            platform: Platform name

        Returns:
            True if supported, False otherwise
        """
        return platform in self.PARSER_MAP

    def is_extension_supported(self, extension: str) -> bool:
        """
        Check if a file extension is supported.

        Args:
            extension: File extension (with or without dot)

        Returns:
            True if supported, False otherwise
        """
        if not extension.startswith('.'):
            extension = '.' + extension
        return extension.lower() in self.EXTENSION_MAP

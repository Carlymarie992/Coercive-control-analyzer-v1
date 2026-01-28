"""Data anonymization tools for privacy protection."""

import re
from typing import Dict, List
import hashlib


class DataAnonymizer:
    """Anonymize sensitive information in text and data."""

    def __init__(self):
        """Initialize anonymizer with pattern matchers."""
        self.name_replacements = {}
        self.phone_replacements = {}
        self.email_replacements = {}
        self.location_replacements = {}

        # Common name patterns (simple detection)
        self.name_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'

        # Phone number patterns
        self.phone_patterns = [
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # US format
            r'\b\(\d{3}\)\s?\d{3}[-.\s]?\d{4}\b',   # (123) 456-7890
            r'\b\+\d{1,3}\s?\d{3,4}[\s.-]?\d{3,4}[\s.-]?\d{3,4}\b'  # International
        ]

        # Email pattern
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        # Address patterns (basic)
        self.address_pattern = r'\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b'

    def anonymize_text(self, text: str, anonymize_names: bool = True,
                       anonymize_phones: bool = True,
                       anonymize_emails: bool = True,
                       anonymize_locations: bool = True) -> str:
        """
        Anonymize sensitive information in text.

        Args:
            text: Text to anonymize
            anonymize_names: Whether to anonymize names
            anonymize_phones: Whether to anonymize phone numbers
            anonymize_emails: Whether to anonymize email addresses
            anonymize_locations: Whether to anonymize locations

        Returns:
            Anonymized text
        """
        result = text

        if anonymize_phones:
            result = self._anonymize_phones(result)

        if anonymize_emails:
            result = self._anonymize_emails(result)

        if anonymize_locations:
            result = self._anonymize_locations(result)

        # Note: Name anonymization is complex and may have false positives
        # Disabled by default for safety
        # if anonymize_names:
        #     result = self._anonymize_names(result)

        return result

    def _anonymize_phones(self, text: str) -> str:
        """Replace phone numbers with anonymized versions."""
        for pattern in self.phone_patterns:
            def replace_phone(match):
                phone = match.group(0)
                if phone not in self.phone_replacements:
                    # Create consistent replacement
                    hash_val = hashlib.md5(phone.encode()).hexdigest()[:4]
                    self.phone_replacements[phone] = f"[PHONE-{hash_val}]"
                return self.phone_replacements[phone]

            text = re.sub(pattern, replace_phone, text)

        return text

    def _anonymize_emails(self, text: str) -> str:
        """Replace email addresses with anonymized versions."""
        def replace_email(match):
            email = match.group(0)
            if email not in self.email_replacements:
                hash_val = hashlib.md5(email.encode()).hexdigest()[:4]
                self.email_replacements[email] = f"[EMAIL-{hash_val}]"
            return self.email_replacements[email]

        return re.sub(self.email_pattern, replace_email, text)

    def _anonymize_locations(self, text: str) -> str:
        """Replace address information with anonymized versions."""
        def replace_location(match):
            location = match.group(0)
            if location not in self.location_replacements:
                hash_val = hashlib.md5(location.encode()).hexdigest()[:4]
                self.location_replacements[location] = f"[ADDRESS-{hash_val}]"
            return self.location_replacements[location]

        return re.sub(self.address_pattern, replace_location, text, flags=re.IGNORECASE)

    def _anonymize_names(self, text: str) -> str:
        """
        Replace potential names with anonymized versions.
        Note: This is basic and may have false positives.
        """
        def replace_name(match):
            name = match.group(0)
            # Skip common words that aren't names
            skip_words = {'The', 'This', 'That', 'These', 'Those', 'When', 'Where',
                          'What', 'Who', 'Why', 'How', 'Monday', 'Tuesday', 'Wednesday',
                          'Thursday', 'Friday', 'Saturday', 'Sunday', 'January', 'February',
                          'March', 'April', 'May', 'June', 'July', 'August', 'September',
                          'October', 'November', 'December'}

            if name in skip_words:
                return name

            if name not in self.name_replacements:
                hash_val = hashlib.md5(name.encode()).hexdigest()[:4]
                self.name_replacements[name] = f"[PERSON-{hash_val}]"
            return self.name_replacements[name]

        return re.sub(self.name_pattern, replace_name, text)

    def anonymize_conversation(self, messages: List[Dict]) -> List[Dict]:
        """
        Anonymize a list of conversation messages.

        Args:
            messages: List of message dictionaries

        Returns:
            List of anonymized messages
        """
        anonymized = []

        for msg in messages:
            anonymized_msg = msg.copy()

            # Anonymize text
            if 'text' in anonymized_msg:
                anonymized_msg['text'] = self.anonymize_text(anonymized_msg['text'])

            # Anonymize sender (use hash)
            if 'sender' in anonymized_msg:
                sender = anonymized_msg['sender']
                if sender not in self.name_replacements:
                    hash_val = hashlib.md5(sender.encode()).hexdigest()[:6]
                    self.name_replacements[sender] = f"User-{hash_val}"
                anonymized_msg['sender'] = self.name_replacements[sender]

            anonymized.append(anonymized_msg)

        return anonymized

    def get_replacement_mapping(self) -> Dict[str, Dict[str, str]]:
        """
        Get mapping of original values to anonymized versions.

        Returns:
            Dictionary of replacement mappings
        """
        return {
            'names': self.name_replacements.copy(),
            'phones': self.phone_replacements.copy(),
            'emails': self.email_replacements.copy(),
            'locations': self.location_replacements.copy()
        }

    def clear_mappings(self):
        """Clear all replacement mappings."""
        self.name_replacements.clear()
        self.phone_replacements.clear()
        self.email_replacements.clear()
        self.location_replacements.clear()

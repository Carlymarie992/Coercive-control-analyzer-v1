import requirements.txt
from typing import List, Dict, Any, Optional
from difflib import SequenceMatcher

class AbusePatternEngine:
    """
    Advanced abuse pattern engine with fuzzy matching, synonym detection, and context analysis.
    """
    def __init__(self, indicators: Dict[str, List[str]], synonyms: Optional[Dict[str, List[str]]] = None):
        self.indicators = indicators
        self.synonyms = synonyms or {}

    def fuzzy_match(self, text: str, keyword: str, threshold: float = 0.85) -> bool:
        """Fuzzy match keyword in text using similarity threshold."""
        return SequenceMatcher(None, text.lower(), keyword.lower()).ratio() >= threshold

    def synonym_match(self, text: str, keyword: str) -> bool:
        """Check if text matches keyword or any of its synonyms."""
        if keyword in self.synonyms:
            for syn in self.synonyms[keyword]:
                if syn in text.lower():
                    return True
        return keyword in text.lower()

    def analyze_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single message for abuse patterns."""
        results = {}
        text = message.get('text', '').lower()
        for category, keywords in self.indicators.items():
            for kw in keywords:
                if self.synonym_match(text, kw) or self.fuzzy_match(text, kw):
                    results.setdefault(category, []).append(kw)
        return results

    def analyze_conversation(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze a list of messages for patterns, escalation, and cycles."""
        pattern_results = {}
        for msg in messages:
            msg_patterns = self.analyze_message(msg)
            for cat, kws in msg_patterns.items():
                pattern_results.setdefault(cat, []).extend(kws)
        # Detect escalation and cycles
        pattern_results['escalation_detected'] = self.detect_escalation(messages)
        pattern_results['cycle_detected'] = self.detect_cycle(messages)
        return pattern_results

    def detect_escalation(self, messages: List[Dict[str, Any]]) -> bool:
        """Detect escalation in abuse patterns over time."""
        # Simple heuristic: increasing frequency or severity
        abuse_counts = [len(self.analyze_message(m)) for m in messages]
        return any(abuse_counts[i] < abuse_counts[i+1] for i in range(len(abuse_counts)-1))

    def detect_cycle(self, messages: List[Dict[str, Any]]) -> bool:
        """Detect repeated cycles of abuse patterns."""
        # Simple heuristic: repeated pattern categories in sequence
        last_cat = None
        cycle_count = 0
        for m in messages:
            cats = list(self.analyze_message(m).keys())
            if cats and cats[0] == last_cat:
                cycle_count += 1
            last_cat = cats[0] if cats else last_cat
        return cycle_count > 2

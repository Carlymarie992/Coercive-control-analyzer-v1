"""
DARVO Tactics Analyzer for Coercive Control Detection.

This module provides comprehensive analysis of DARVO (Deny, Attack, and Reverse
Victim and Offender) manipulation tactics in communications and documents.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from collections import defaultdict, Counter
import re

from darvo_indicators import (
    DARVO_INDICATORS,
    DARVO_COMPOUND_PATTERNS,
    DARVO_SEVERITY_WEIGHTS,
    CHILD_FOCUSED_DARVO
)


class DARVOAnalyzer:
    """Analyzer for detecting DARVO manipulation tactics."""

    def __init__(self, messages: Optional[List[Dict]] = None, text: Optional[str] = None):
        """
        Initialize DARVO analyzer.

        Args:
            messages: List of message dictionaries (for conversation analysis)
            text: Plain text string (for document analysis)
        """
        self.messages = messages or []
        self.text = text or ""
        self.darvo_patterns = {}
        self.severity_score = 0
        self.timeline_events = []
        self.compound_patterns_found = []
        
    def analyze_darvo_patterns(self) -> Dict:
        """
        Comprehensive DARVO pattern analysis.

        Returns:
            Dictionary containing all DARVO analysis results
        """
        if self.messages:
            return self._analyze_conversation()
        elif self.text:
            return self._analyze_document()
        else:
            # Return empty structure for empty input
            return {
                "deny_patterns": {},
                "attack_patterns": {},
                "reverse_patterns": {},
                "institutional_patterns": {},
                "child_focused_patterns": {},
                "compound_patterns": [],
                "severity_assessment": {
                    "total_score": 0,
                    "category_scores": {},
                    "risk_level": "low",
                    "interpretation": "No data available for analysis."
                },
                "timeline_analysis": {"timeline_available": False},
                "forensic_summary": {
                    "analysis_date": datetime.now().isoformat(),
                    "total_messages_analyzed": 0,
                    "darvo_components_present": {
                        "deny": False,
                        "attack": False,
                        "reverse": False
                    },
                    "full_darvo_pattern_detected": False,
                    "instance_counts": {
                        "deny_instances": 0,
                        "attack_instances": 0,
                        "reverse_instances": 0,
                        "child_focused_instances": 0
                    },
                    "high_risk_indicators": False,
                    "recommended_actions": []
                }
            }

    def _analyze_conversation(self) -> Dict:
        """Analyze DARVO patterns in conversation messages."""
        results = {
            "deny_patterns": self._detect_deny_patterns(),
            "attack_patterns": self._detect_attack_patterns(),
            "reverse_patterns": self._detect_reverse_patterns(),
            "institutional_patterns": self._detect_institutional_patterns(),
            "child_focused_patterns": self._detect_child_focused_patterns(),
            "compound_patterns": self._detect_compound_patterns(),
            "severity_assessment": self._calculate_severity(),
            "timeline_analysis": self._analyze_timeline(),
            "forensic_summary": self._generate_forensic_summary()
        }
        
        return results

    def _analyze_document(self) -> Dict:
        """Analyze DARVO patterns in document text."""
        # Convert text to message-like structure for unified processing
        self.messages = [{
            'text': self.text,
            'sender': 'Document',
            'timestamp': datetime.now(),
            'platform': 'document'
        }]
        
        return self._analyze_conversation()

    def _detect_deny_patterns(self) -> Dict:
        """Detect denial patterns in messages."""
        deny_results = {
            "minimization": {"count": 0, "instances": []},
            "outright_denial": {"count": 0, "instances": []},
            "blame_shifting": {"count": 0, "instances": []}
        }
        
        for msg in self.messages:
            text = msg.get('text', '').lower()
            timestamp = msg.get('timestamp')
            sender = msg.get('sender', 'Unknown')
            
            for subcategory, keywords in DARVO_INDICATORS["Deny"].items():
                for keyword in keywords:
                    pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                    if re.search(pattern, text):
                        deny_results[subcategory]["count"] += 1
                        deny_results[subcategory]["instances"].append({
                            "keyword": keyword,
                            "text": msg.get('text', '')[:200],
                            "sender": sender,
                            "timestamp": timestamp.isoformat() if timestamp else None,
                            "severity": DARVO_SEVERITY_WEIGHTS["Deny"][subcategory]
                        })
                        break  # Count each message once per subcategory
        
        return deny_results

    def _detect_attack_patterns(self) -> Dict:
        """Detect attack patterns in messages."""
        attack_results = {
            "credibility_attacks": {"count": 0, "instances": []},
            "character_assassination": {"count": 0, "instances": []},
            "threat_of_consequences": {"count": 0, "instances": []},
            "gaslighting": {"count": 0, "instances": []}
        }
        
        for msg in self.messages:
            text = msg.get('text', '').lower()
            timestamp = msg.get('timestamp')
            sender = msg.get('sender', 'Unknown')
            
            for subcategory, keywords in DARVO_INDICATORS["Attack"].items():
                for keyword in keywords:
                    pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                    if re.search(pattern, text):
                        attack_results[subcategory]["count"] += 1
                        attack_results[subcategory]["instances"].append({
                            "keyword": keyword,
                            "text": msg.get('text', '')[:200],
                            "sender": sender,
                            "timestamp": timestamp.isoformat() if timestamp else None,
                            "severity": DARVO_SEVERITY_WEIGHTS["Attack"][subcategory]
                        })
                        break
        
        return attack_results

    def _detect_reverse_patterns(self) -> Dict:
        """Detect victim/offender reversal patterns."""
        reverse_results = {
            "self_victimization": {"count": 0, "instances": []},
            "victim_blaming": {"count": 0, "instances": []},
            "false_equivalence": {"count": 0, "instances": []},
            "protective_parent_reversal": {"count": 0, "instances": []}
        }
        
        for msg in self.messages:
            text = msg.get('text', '').lower()
            timestamp = msg.get('timestamp')
            sender = msg.get('sender', 'Unknown')
            
            for subcategory, keywords in DARVO_INDICATORS["Reverse_Victim_Offender"].items():
                for keyword in keywords:
                    pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                    if re.search(pattern, text):
                        reverse_results[subcategory]["count"] += 1
                        reverse_results[subcategory]["instances"].append({
                            "keyword": keyword,
                            "text": msg.get('text', '')[:200],
                            "sender": sender,
                            "timestamp": timestamp.isoformat() if timestamp else None,
                            "severity": DARVO_SEVERITY_WEIGHTS["Reverse_Victim_Offender"][subcategory]
                        })
                        break
        
        return reverse_results

    def _detect_institutional_patterns(self) -> Dict:
        """Detect institutional/legal DARVO patterns."""
        institutional_results = {
            "court_manipulation": {"count": 0, "instances": []},
            "professional_credibility": {"count": 0, "instances": []},
            "systemic_bias_indicators": {"count": 0, "instances": []}
        }
        
        for msg in self.messages:
            text = msg.get('text', '').lower()
            timestamp = msg.get('timestamp')
            sender = msg.get('sender', 'Unknown')
            
            for subcategory, keywords in DARVO_INDICATORS["Institutional_DARVO"].items():
                for keyword in keywords:
                    pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                    if re.search(pattern, text):
                        institutional_results[subcategory]["count"] += 1
                        institutional_results[subcategory]["instances"].append({
                            "keyword": keyword,
                            "text": msg.get('text', '')[:200],
                            "sender": sender,
                            "timestamp": timestamp.isoformat() if timestamp else None,
                            "severity": DARVO_SEVERITY_WEIGHTS["Institutional_DARVO"][subcategory]
                        })
                        break
        
        return institutional_results

    def _detect_child_focused_patterns(self) -> Dict:
        """Detect child-focused DARVO patterns (high priority)."""
        child_results = {
            "child_weaponization": {"count": 0, "instances": []},
            "parental_alienation_claims": {"count": 0, "instances": []},
            "custody_threats": {"count": 0, "instances": []}
        }
        
        for msg in self.messages:
            text = msg.get('text', '').lower()
            timestamp = msg.get('timestamp')
            sender = msg.get('sender', 'Unknown')
            
            for subcategory, keywords in CHILD_FOCUSED_DARVO.items():
                for keyword in keywords:
                    pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                    if re.search(pattern, text):
                        child_results[subcategory]["count"] += 1
                        child_results[subcategory]["instances"].append({
                            "keyword": keyword,
                            "text": msg.get('text', '')[:200],
                            "sender": sender,
                            "timestamp": timestamp.isoformat() if timestamp else None,
                            "severity": 5,  # Child-related patterns always high severity
                            "high_risk": True
                        })
                        break
        
        return child_results

    def _detect_compound_patterns(self) -> List[Dict]:
        """
        Detect compound DARVO patterns (sequences of deny->attack->reverse).
        
        Returns:
            List of compound patterns found
        """
        compound_patterns = []
        
        if len(self.messages) < 2:
            return compound_patterns
        
        # Classify each message
        message_classifications = []
        for msg in self.messages:
            text = msg.get('text', '').lower()
            classifications = []
            
            # Check for deny
            if any(re.search(r'\b' + re.escape(kw.lower()) + r'\b', text) 
                   for subcat in DARVO_INDICATORS["Deny"].values() 
                   for kw in subcat):
                classifications.append('deny')
            
            # Check for attack
            if any(re.search(r'\b' + re.escape(kw.lower()) + r'\b', text) 
                   for subcat in DARVO_INDICATORS["Attack"].values() 
                   for kw in subcat):
                classifications.append('attack')
            
            # Check for reverse
            if any(re.search(r'\b' + re.escape(kw.lower()) + r'\b', text) 
                   for subcat in DARVO_INDICATORS["Reverse_Victim_Offender"].values() 
                   for kw in subcat):
                classifications.append('reverse')
            
            message_classifications.append({
                'classifications': classifications,
                'message': msg
            })
        
        # Look for compound patterns
        for pattern_name, pattern_def in DARVO_COMPOUND_PATTERNS.items():
            window_size = pattern_def["window_messages"]
            target_pattern = pattern_def["pattern"]
            
            for i in range(len(message_classifications) - len(target_pattern) + 1):
                window = message_classifications[i:i + window_size]
                
                # Check if pattern appears in window
                pattern_found = self._check_pattern_in_window(window, target_pattern)
                
                if pattern_found:
                    compound_patterns.append({
                        "pattern_type": pattern_name,
                        "description": pattern_def["description"],
                        "messages": [w['message'] for w in window if w['classifications']],
                        "severity": len(target_pattern) * 2,  # Higher severity for compound patterns
                        "start_time": window[0]['message'].get('timestamp'),
                        "end_time": window[-1]['message'].get('timestamp')
                    })
        
        return compound_patterns

    def _check_pattern_in_window(self, window: List[Dict], target_pattern: List[str]) -> bool:
        """Check if a target pattern sequence appears in a message window."""
        pattern_index = 0
        
        for msg_class in window:
            if pattern_index < len(target_pattern):
                if target_pattern[pattern_index] in msg_class['classifications']:
                    pattern_index += 1
        
        return pattern_index == len(target_pattern)

    def _calculate_severity(self) -> Dict:
        """
        Calculate overall DARVO severity score.
        
        Returns:
            Dictionary with severity assessment
        """
        total_score = 0
        category_scores = {
            "deny": 0,
            "attack": 0,
            "reverse": 0,
            "institutional": 0,
            "child_focused": 0
        }
        
        # Calculate from detected patterns
        for msg in self.messages:
            text = msg.get('text', '').lower()
            
            # Score denial patterns
            for subcat, keywords in DARVO_INDICATORS["Deny"].items():
                for keyword in keywords:
                    if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text):
                        score = DARVO_SEVERITY_WEIGHTS["Deny"][subcat]
                        category_scores["deny"] += score
                        total_score += score
                        break
            
            # Score attack patterns
            for subcat, keywords in DARVO_INDICATORS["Attack"].items():
                for keyword in keywords:
                    if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text):
                        score = DARVO_SEVERITY_WEIGHTS["Attack"][subcat]
                        category_scores["attack"] += score
                        total_score += score
                        break
            
            # Score reverse patterns
            for subcat, keywords in DARVO_INDICATORS["Reverse_Victim_Offender"].items():
                for keyword in keywords:
                    if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text):
                        score = DARVO_SEVERITY_WEIGHTS["Reverse_Victim_Offender"][subcat]
                        category_scores["reverse"] += score
                        total_score += score
                        break
            
            # Score institutional patterns
            for subcat, keywords in DARVO_INDICATORS["Institutional_DARVO"].items():
                for keyword in keywords:
                    if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text):
                        score = DARVO_SEVERITY_WEIGHTS["Institutional_DARVO"][subcat]
                        category_scores["institutional"] += score
                        total_score += score
                        break
            
            # Score child-focused patterns (always severity 5)
            for keywords in CHILD_FOCUSED_DARVO.values():
                for keyword in keywords:
                    if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text):
                        category_scores["child_focused"] += 5
                        total_score += 5
                        break
        
        # Determine risk level
        risk_level = "low"
        if total_score > 50:
            risk_level = "critical"
        elif total_score > 30:
            risk_level = "high"
        elif total_score > 15:
            risk_level = "medium"
        
        # Child-focused patterns elevate risk to critical
        if category_scores["child_focused"] > 0:
            risk_level = "critical"
        
        return {
            "total_score": total_score,
            "category_scores": category_scores,
            "risk_level": risk_level,
            "interpretation": self._interpret_severity(risk_level, total_score)
        }

    def _interpret_severity(self, risk_level: str, score: int) -> str:
        """Provide interpretation of severity score."""
        interpretations = {
            "low": f"Low-level DARVO indicators detected (score: {score}). Some manipulation tactics present but not systematic.",
            "medium": f"Moderate DARVO pattern presence (score: {score}). Multiple manipulation tactics detected across categories.",
            "high": f"Significant DARVO tactics identified (score: {score}). Systematic pattern of deny, attack, and reversal behaviors.",
            "critical": f"Critical DARVO pattern severity (score: {score}). Extensive manipulation tactics including high-risk child-focused patterns."
        }
        return interpretations.get(risk_level, "Unable to determine severity.")

    def _analyze_timeline(self) -> Dict:
        """Analyze DARVO patterns over time."""
        if not self.messages or not any(m.get('timestamp') for m in self.messages):
            return {"timeline_available": False}
        
        # Group patterns by time windows
        time_windows = defaultdict(lambda: {
            "deny_count": 0,
            "attack_count": 0,
            "reverse_count": 0,
            "total_score": 0
        })
        
        for msg in self.messages:
            if not msg.get('timestamp'):
                continue
            
            # Use weekly windows
            timestamp = msg.get('timestamp')
            week_start = timestamp - timedelta(days=timestamp.weekday())
            week_key = week_start.strftime('%Y-%m-%d')
            
            text = msg.get('text', '').lower()
            
            # Count patterns in this window
            if any(re.search(r'\b' + re.escape(kw.lower()) + r'\b', text) 
                   for subcat in DARVO_INDICATORS["Deny"].values() for kw in subcat):
                time_windows[week_key]["deny_count"] += 1
            
            if any(re.search(r'\b' + re.escape(kw.lower()) + r'\b', text) 
                   for subcat in DARVO_INDICATORS["Attack"].values() for kw in subcat):
                time_windows[week_key]["attack_count"] += 1
            
            if any(re.search(r'\b' + re.escape(kw.lower()) + r'\b', text) 
                   for subcat in DARVO_INDICATORS["Reverse_Victim_Offender"].values() for kw in subcat):
                time_windows[week_key]["reverse_count"] += 1
        
        # Detect escalation
        sorted_weeks = sorted(time_windows.keys())
        escalation_detected = False
        
        if len(sorted_weeks) >= 2:
            early_counts = time_windows[sorted_weeks[0]]
            late_counts = time_windows[sorted_weeks[-1]]
            early_total = early_counts["deny_count"] + early_counts["attack_count"] + early_counts["reverse_count"]
            late_total = late_counts["deny_count"] + late_counts["attack_count"] + late_counts["reverse_count"]
            if late_total > early_total * 1.5:
                escalation_detected = True
        
        return {
            "timeline_available": True,
            "time_windows": dict(time_windows),
            "escalation_detected": escalation_detected,
            "total_weeks": len(sorted_weeks)
        }

    def _generate_forensic_summary(self) -> Dict:
        """
        Generate forensic summary suitable for legal documentation.
        
        Returns:
            Dictionary with court-ready summary
        """
        # Count total message instances (not keyword occurrences)
        messages_with_deny = set()
        messages_with_attack = set()
        messages_with_reverse = set()
        messages_with_child = set()
        
        for i, msg in enumerate(self.messages):
            text = msg.get('text', '').lower()
            
            # Check for deny patterns
            if any(
                re.search(r'\b' + re.escape(kw.lower()) + r'\b', text)
                for keywords in DARVO_INDICATORS["Deny"].values()
                for kw in keywords
            ):
                messages_with_deny.add(i)
            
            # Check for attack patterns
            if any(
                re.search(r'\b' + re.escape(kw.lower()) + r'\b', text)
                for keywords in DARVO_INDICATORS["Attack"].values()
                for kw in keywords
            ):
                messages_with_attack.add(i)
            
            # Check for reverse patterns
            if any(
                re.search(r'\b' + re.escape(kw.lower()) + r'\b', text)
                for keywords in DARVO_INDICATORS["Reverse_Victim_Offender"].values()
                for kw in keywords
            ):
                messages_with_reverse.add(i)
            
            # Check for child-focused patterns
            if any(
                re.search(r'\b' + re.escape(kw.lower()) + r'\b', text)
                for keywords in CHILD_FOCUSED_DARVO.values()
                for kw in keywords
            ):
                messages_with_child.add(i)
        
        total_deny = len(messages_with_deny)
        total_attack = len(messages_with_attack)
        total_reverse = len(messages_with_reverse)
        total_child_focused = len(messages_with_child)
        
        # Determine if full DARVO pattern present
        full_pattern_present = total_deny > 0 and total_attack > 0 and total_reverse > 0
        
        return {
            "analysis_date": datetime.now().isoformat(),
            "total_messages_analyzed": len(self.messages),
            "darvo_components_present": {
                "deny": total_deny > 0,
                "attack": total_attack > 0,
                "reverse": total_reverse > 0
            },
            "full_darvo_pattern_detected": full_pattern_present,
            "instance_counts": {
                "deny_instances": total_deny,
                "attack_instances": total_attack,
                "reverse_instances": total_reverse,
                "child_focused_instances": total_child_focused
            },
            "high_risk_indicators": total_child_focused > 0,
            "recommended_actions": self._generate_recommendations(
                full_pattern_present, total_child_focused > 0
            )
        }

    def _generate_recommendations(self, full_pattern: bool, child_risk: bool) -> List[str]:
        """Generate recommendations based on findings."""
        recommendations = []
        
        if full_pattern:
            recommendations.append(
                "Document all communications for legal proceedings"
            )
            recommendations.append(
                "Consider consultation with domestic violence advocate"
            )
        
        if child_risk:
            recommendations.append(
                "URGENT: Child-focused manipulation detected - consider immediate protective measures"
            )
            recommendations.append(
                "Document all child-related statements for custody proceedings"
            )
            recommendations.append(
                "Consult with family law attorney regarding parental alienation concerns"
            )
        
        if not recommendations:
            recommendations.append(
                "Continue monitoring communications for patterns"
            )
        
        return recommendations

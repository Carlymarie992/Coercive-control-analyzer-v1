#!/usr/bin/env python3
"""
Example: DARVO Tactics Analysis

This script demonstrates how to use the DARVO analyzer to detect manipulation
patterns in communications. DARVO (Deny, Attack, and Reverse Victim and Offender)
is a common pattern used by abusers, particularly in legal contexts.

Run: python examples/darvo_analysis_example.py
"""

from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conversation_analyzer import ConversationAnalyzer
from darvo_analyzer import DARVOAnalyzer


def main():
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "DARVO ANALYSIS EXAMPLE" + " " * 36 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Sample messages with DARVO patterns
    messages = [
        {
            'timestamp': datetime(2024, 1, 1, 10, 0),
            'sender': 'Abuser',
            'text': 'I never said that. You are making things up.',
            'platform': 'email'
        },
        {
            'timestamp': datetime(2024, 1, 1, 10, 5),
            'sender': 'Abuser',
            'text': "You're crazy and nobody will believe you.",
            'platform': 'email'
        },
        {
            'timestamp': datetime(2024, 1, 1, 10, 10),
            'sender': 'Abuser',
            'text': "I'm the victim here. You're abusing me.",
            'platform': 'email'
        },
        {
            'timestamp': datetime(2024, 1, 1, 10, 15),
            'sender': 'Abuser',
            'text': "The children are afraid of you.",
            'platform': 'email'
        }
    ]
    
    print("Analyzing 4 sample messages for DARVO patterns...\n")
    
    # Create analyzer
    analyzer = DARVOAnalyzer(messages=messages)
    results = analyzer.analyze_darvo_patterns()
    
    # Display results
    print("=" * 80)
    print("DARVO COMPONENTS DETECTED")
    print("=" * 80)
    print(f"Deny patterns: {results['deny_patterns']['outright_denial']['count']} instances")
    print(f"Attack patterns: {results['attack_patterns']['credibility_attacks']['count']} instances")
    print(f"Reverse patterns: {results['reverse_patterns']['self_victimization']['count']} instances")
    
    # Display severity
    severity = results['severity_assessment']
    print(f"\n{'=' * 80}")
    print("RISK ASSESSMENT")
    print("=" * 80)
    print(f"Risk Level: {severity['risk_level'].upper()}")
    print(f"Severity Score: {severity['total_score']}")
    print(f"\n{severity['interpretation']}")
    
    # Display forensic summary
    forensic = results['forensic_summary']
    if forensic['full_darvo_pattern_detected']:
        print(f"\n{'!' * 80}")
        print("⚠ ALERT: Complete DARVO pattern detected")
        print("All components present: Deny, Attack, and Reverse Victim/Offender")
        print("!" * 80)
    
    # Check for child-focused patterns
    if forensic['high_risk_indicators']:
        print(f"\n{'!' * 80}")
        print("🚨 HIGH RISK: Child-focused manipulation detected")
        print(f"Child-focused instances: {forensic['instance_counts']['child_focused_instances']}")
        print("!" * 80)
        
        print("\nRECOMMENDED ACTIONS:")
        for action in forensic['recommended_actions']:
            print(f"  • {action}")
    
    print(f"\n{'=' * 80}")
    print("For detailed reports, use:")
    print("  python cli.py analyze <file> --format html")
    print("=" * 80)
    print()


if __name__ == '__main__':
    main()

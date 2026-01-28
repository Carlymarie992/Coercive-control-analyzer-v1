import argparse
import sys
import re
from pypdf import PdfReader
from abuse_pattern_engine import AbusePatternEngine
from abuse_indicators import ABUSE_INDICATORS

# Example synonym mapping (expand as needed)
ABUSE_SYNONYMS = {
    "gaslighting": ["crazy-making", "mind games", "tripping", "confuse", "you're crazy", "you're imagining things", "you're paranoid"],
    "threaten": ["warn", "promise harm", "intimidate", "menace", "bully", "scare", "coerce", "blackmail"],
    "money": ["cash", "venmo", "bank", "finesse", "allowance", "paycheck", "salary", "income", "funds", "debt", "loan"],
    "isolate": ["cut off", "block", "ghost", "no contact", "keep away", "ban", "forbid", "separate", "alienate"],
    "emotional abuse": ["put-downs", "insult", "mock", "humiliate", "demean", "shame", "guilt trip", "belittle", "criticize"],
    "sexual coercion": ["pressure for sex", "forced intimacy", "unwanted touch", "sexual assault", "revenge porn", "nudes", "sext"],
    "digital abuse": ["spyware", "track", "monitor", "hack", "impersonate", "catfish", "dox", "cyberbully", "harass online"],
    # Add more synonyms/slang as needed
}

def extract_text_from_pdf(filepath: str) -> str | None:
    """
    Extracts text from a PDF file.

    Args:
        filepath (str): The path to the PDF file.

    Returns:
        str: The extracted text.
    """
    try:
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            result = page.extract_text()
            if result:
                text += result + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None

def normalize_text(text: str) -> str:
    """
    Normalizes text by replacing smart quotes and other common characters
    that might interfere with matching.
    """
    # Replace smart quotes with straight quotes
    text = text.replace('‘', "'").replace('’', "'")
    text = text.replace('“', '"').replace('”', '"')
    return text

from typing import Dict, List, Any
def analyze_text(messages: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Scans structured messages for abuse indicators, including sender, receiver, id, timestamp, and full message.
    Orders findings chronologically and includes placeholders for file, line, and page number.
    """
    from difflib import SequenceMatcher
    results = {}
    context_window = 40
    findings = []
    for msg in messages:
        text = normalize_text(msg.get('text', ''))
        lower_text = text.lower()
        sender = msg.get('sender', 'Unknown')
        receiver = msg.get('receiver', 'Unknown')
        msg_id = msg.get('id', None)
        timestamp = msg.get('timestamp', None)
        file = msg.get('file', None)
        line_number = msg.get('line_number', None)
        page_number = msg.get('page_number', None)
        for category, keywords in ABUSE_INDICATORS.items():
            for keyword in keywords:
                # Regex match
                escaped_keyword = re.escape(keyword)
                pattern = r'\b' + escaped_keyword + r'\b'
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    findings.append({
                        'category': category,
                        'indicator': keyword,
                        'type': 'exact',
                        'context': text[max(0, match.start()-context_window):match.end()+context_window],
                        'full_message': text,
                        'sender': sender,
                        'receiver': receiver,
                        'id': msg_id,
                        'timestamp': timestamp,
                        'file': file,
                        'line_number': line_number,
                        'page_number': page_number
                    })
                # Fuzzy match
                for i in range(len(lower_text) - len(keyword) + 1):
                    window = lower_text[i:i+len(keyword)]
                    if SequenceMatcher(None, window, keyword.lower()).ratio() > 0.85:
                        findings.append({
                            'category': category,
                            'indicator': keyword,
                            'type': 'fuzzy',
                            'context': text[max(0, i-context_window):i+len(keyword)+context_window],
                            'full_message': text,
                            'sender': sender,
                            'receiver': receiver,
                            'id': msg_id,
                            'timestamp': timestamp,
                            'file': file,
                            'line_number': line_number,
                            'page_number': page_number
                        })
                        break
                # Synonym match
                for syn, syn_list in ABUSE_SYNONYMS.items():
                    if keyword.lower() == syn.lower():
                        for syn_kw in syn_list:
                            syn_pattern = r'\b' + re.escape(syn_kw) + r'\b'
                            for match in re.finditer(syn_pattern, text, re.IGNORECASE):
                                findings.append({
                                    'category': category,
                                    'indicator': syn_kw,
                                    'type': 'synonym',
                                    'context': text[max(0, match.start()-context_window):match.end()+context_window],
                                    'full_message': text,
                                    'sender': sender,
                                    'receiver': receiver,
                                    'id': msg_id,
                                    'timestamp': timestamp,
                                    'file': file,
                                    'line_number': line_number,
                                    'page_number': page_number
                                })
    # Order findings chronologically if timestamp is present
    findings.sort(key=lambda x: x.get('timestamp') or '')
    # Group by category
    for finding in findings:
        results.setdefault(finding['category'], []).append(finding)
    # Escalation: if multiple categories or many indicators found
    escalation = False
    if len(results) > 2 or sum(len(v) for v in results.values()) > 10:
        escalation = True
    results['escalation_detected'] = escalation
    return results

def analyze_text_advanced(text: str) -> Dict[str, Any]:
    """
    Advanced analysis using fuzzy matching, synonyms, and context-aware engine.
    """
    engine = AbusePatternEngine(ABUSE_INDICATORS, ABUSE_SYNONYMS)
    # For PDF, treat as one message
    message = {"text": text}
    return engine.analyze_message(message)

def print_results(results: Dict[str, Any]) -> None:
    """
    Prints the analysis results in a readable format.

    Args:
        results (dict): The analysis results.
    """
    if not results or all(k == 'escalation_detected' for k in results):
        print("No specific abuse patterns detected based on the current indicators.")
        return

    print("--- Abuse Pattern Analysis Results (Chronological) ---\n")
    for category, found_list in results.items():
        if category == 'escalation_detected':
            continue
        print(f"Category: {category}")
        for item in found_list:
            print(f"  Indicator: {item['indicator']} (type: {item['type']})")
            print(f"    Sender: {item.get('sender', 'Unknown')}  Receiver: {item.get('receiver', 'Unknown')}")
            print(f"    ID: {item.get('id', '')}  Timestamp: {item.get('timestamp', '')}")
            print(f"    File: {item.get('file', '')}  Line: {item.get('line_number', '')}  Page: {item.get('page_number', '')}")
            print(f"    Full Message: {item.get('full_message', '')}")
            print(f"    Context: ...{item['context']}...")
        print(f"  Count: {len(found_list)}\n")
    if results.get('escalation_detected'):
        print("*** Escalation detected: Multiple categories or high indicator count. ***\n")

def main():
    parser = argparse.ArgumentParser(description="Analyze a PDF for patterns of coercive control.")
    parser.add_argument("input_file", help="Path to the PDF file to analyze.")
    parser.add_argument("--advanced", action="store_true", help="Use advanced pattern engine.")
    args = parser.parse_args()

    print(f"Analyzing {args.input_file}...")

    text = extract_text_from_pdf(args.input_file)

    if text:
        if args.advanced:
            results = analyze_text_advanced(text)
            print("--- Advanced Abuse Pattern Engine Results ---\n")
        else:
            results = analyze_text(text)
            print("--- Basic Abuse Pattern Analysis Results ---\n")
        print_results(results)
    else:
        print("Could not extract text from file.")
        sys.exit(1)

if __name__ == "__main__":
    main()

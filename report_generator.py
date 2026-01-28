"""Report generation for coercive control analysis."""

import json
import base64
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from jinja2 import Template

from visualizations import AnalysisVisualizations
from config.settings import DEFAULT_REPORT_FORMAT


class ReportGenerator:
    """Generate comprehensive analysis reports."""

    def __init__(self, output_dir: str = 'output'):
        """
        Initialize report generator.

        Args:
            output_dir: Directory for output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.viz_generator = AnalysisVisualizations(str(self.output_dir))
    
    def _get_logo_base64(self) -> Optional[str]:
        """
        Get logo as base64 encoded string for embedding in HTML.
        
        Returns:
            Base64 encoded logo or None if not found
        """
        # Try to find logo in assets directory
        logo_paths = [
            Path(__file__).parent / 'assets' / 'logos' / 'logo-small.png',
            Path(__file__).parent / 'assets' / 'logos' / 'logo.png',
        ]
        
        for logo_path in logo_paths:
            if logo_path.exists():
                try:
                    with open(logo_path, 'rb') as f:
                        logo_data = base64.b64encode(f.read()).decode('utf-8')
                        return f"data:image/png;base64,{logo_data}"
                except (IOError, OSError) as e:
                    # Log error but continue trying other logo paths
                    print(f"Warning: Could not read logo file {logo_path}: {e}")
                    continue
        
        return None

    def generate_report(self, analysis_data: Dict, format: Optional[str] = None,
                        output_filename: Optional[str] = None) -> str:
        """
        Generate analysis report.

        Args:
            analysis_data: Analysis results
            format: Report format (html, json, txt)
            output_filename: Custom output filename

        Returns:
            Path to generated report
        """
        format = format or DEFAULT_REPORT_FORMAT

        if not output_filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f'report_{timestamp}.{format}'

        output_path = self.output_dir / output_filename

        if format == 'html':
            return self._generate_html_report(analysis_data, output_path)
        elif format == 'json':
            return self._generate_json_report(analysis_data, output_path)
        elif format == 'txt':
            return self._generate_text_report(analysis_data, output_path)
        else:
            raise ValueError(f"Unsupported report format: {format}")

    def _generate_html_report(self, data: Dict, output_path: Path) -> str:
        """Generate HTML report."""
        # Generate visualizations
        visualizations = self.viz_generator.generate_all_visualizations(data)

        # Create HTML template
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coercive Control Analysis Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background-color: #2c3e50;
            color: white;
            padding: 30px;
            border-radius: 5px;
            margin-bottom: 30px;
            text-align: center;
        }
        .header .logo {
            max-width: 120px;
            height: auto;
            margin-bottom: 15px;
        }
        .header h1 {
            margin: 10px 0 5px 0;
        }
        .header .tagline {
            color: #3498db;
            font-style: italic;
            font-size: 0.9em;
            margin: 5px 0;
        }
        .section {
            background-color: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        .warning {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
        }
        .danger {
            background-color: #f8d7da;
            border-left: 4px solid #dc3545;
            padding: 15px;
            margin: 15px 0;
        }
        .info {
            background-color: #d1ecf1;
            border-left: 4px solid #17a2b8;
            padding: 15px;
            margin: 15px 0;
        }
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-box {
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }
        .stat-label {
            color: #7f8c8d;
            margin-top: 5px;
        }
        .visualization {
            margin: 20px 0;
            text-align: center;
        }
        .visualization img {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #3498db;
            color: white;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: #7f8c8d;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="header">
        {% if logo_data %}
        <img src="{{ logo_data }}" alt="Coercive Control Analyzer" class="logo">
        {% endif %}
        <h1>Coercive Control Analysis Report</h1>
        <p class="tagline">Personal Development</p>
        <p>Generated: {{ timestamp }}</p>
        <p>File: {{ filepath }}</p>
    </div>

    {% if analysis_type == 'conversation_analysis' %}
    <!-- Conversation Analysis Report -->
    <div class="section">
        <h2>Overview</h2>
        <div class="stat-grid">
            <div class="stat-box">
                <div class="stat-value">{{ message_count }}</div>
                <div class="stat-label">Total Messages</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{{ time_span_days }}</div>
                <div class="stat-label">Days Covered</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{{ abuse_pattern_count }}</div>
                <div class="stat-label">Abuse Categories</div>
            </div>
        </div>
    </div>

    {% if escalation_detected %}
    <div class="danger">
        <strong>⚠ ESCALATION PATTERN DETECTED</strong>
        <p>Analysis indicates an escalation in concerning behaviors over time.</p>
    </div>
    {% endif %}

    {% if darvo_tactics %}
    <div class="section">
        <h2>DARVO Tactics Analysis</h2>
        
        {% if darvo_tactics.severity_assessment %}
        <div class="{% if darvo_tactics.severity_assessment.risk_level == 'critical' %}danger{% elif darvo_tactics.severity_assessment.risk_level == 'high' %}warning{% else %}info{% endif %}">
            <strong>Risk Level: {{ darvo_tactics.severity_assessment.risk_level|upper }}</strong>
            <p>{{ darvo_tactics.severity_assessment.interpretation }}</p>
            <p>Total Severity Score: {{ darvo_tactics.severity_assessment.total_score }}</p>
        </div>
        {% endif %}

        {% if darvo_tactics.forensic_summary and darvo_tactics.forensic_summary.full_darvo_pattern_detected %}
        <div class="danger">
            <strong>⚠ COMPLETE DARVO PATTERN DETECTED</strong>
            <p>All three components of DARVO manipulation are present: Deny, Attack, and Reverse Victim/Offender</p>
        </div>
        {% endif %}

        {% if darvo_tactics.child_focused_patterns %}
        {% set child_total = darvo_tactics.child_focused_patterns.child_weaponization.count + darvo_tactics.child_focused_patterns.parental_alienation_claims.count + darvo_tactics.child_focused_patterns.custody_threats.count %}
        {% if child_total > 0 %}
        <div class="danger">
            <strong>🚨 HIGH RISK: CHILD-FOCUSED MANIPULATION DETECTED</strong>
            <p>{{ child_total }} instances of child-focused DARVO tactics identified</p>
        </div>
        {% endif %}
        {% endif %}

        <h3>DARVO Components Detected</h3>
        <table>
            <thead>
                <tr>
                    <th>Component</th>
                    <th>Subcategory</th>
                    <th>Count</th>
                </tr>
            </thead>
            <tbody>
            {% if darvo_tactics.deny_patterns %}
                {% for subcat, data in darvo_tactics.deny_patterns.items() %}
                {% if data.count > 0 %}
                <tr>
                    <td><strong>DENY</strong></td>
                    <td>{{ subcat|replace('_', ' ')|title }}</td>
                    <td>{{ data.count }}</td>
                </tr>
                {% endif %}
                {% endfor %}
            {% endif %}
            
            {% if darvo_tactics.attack_patterns %}
                {% for subcat, data in darvo_tactics.attack_patterns.items() %}
                {% if data.count > 0 %}
                <tr>
                    <td><strong>ATTACK</strong></td>
                    <td>{{ subcat|replace('_', ' ')|title }}</td>
                    <td>{{ data.count }}</td>
                </tr>
                {% endif %}
                {% endfor %}
            {% endif %}
            
            {% if darvo_tactics.reverse_patterns %}
                {% for subcat, data in darvo_tactics.reverse_patterns.items() %}
                {% if data.count > 0 %}
                <tr>
                    <td><strong>REVERSE</strong></td>
                    <td>{{ subcat|replace('_', ' ')|title }}</td>
                    <td>{{ data.count }}</td>
                </tr>
                {% endif %}
                {% endfor %}
            {% endif %}
            </tbody>
        </table>

        {% if darvo_tactics.compound_patterns and darvo_tactics.compound_patterns|length > 0 %}
        <div class="warning">
            <strong>Compound DARVO Sequences Detected: {{ darvo_tactics.compound_patterns|length }}</strong>
            <p>Multiple DARVO tactics appearing in sequence, indicating systematic manipulation.</p>
        </div>
        {% endif %}

        {% if darvo_tactics.forensic_summary and darvo_tactics.forensic_summary.recommended_actions %}
        <h3>Recommended Actions</h3>
        <ul>
        {% for action in darvo_tactics.forensic_summary.recommended_actions %}
            <li>{{ action }}</li>
        {% endfor %}
        </ul>
        {% endif %}
    </div>
    {% endif %}

    {% if abuse_patterns %}
    <div class="section">
        <h2>Abuse Patterns Detected</h2>
        <table>
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Occurrences</th>
                    <th>Indicators</th>
                </tr>
            </thead>
            <tbody>
            {% for category, data in abuse_patterns.items() %}
                <tr>
                    <td><strong>{{ category }}</strong></td>
                    <td>{{ data.count }}</td>
                    <td>{{ data.keywords|join(', ') }}</td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
    {% endif %}

    {% elif analysis_type == 'document_analysis' %}
    <!-- Document Analysis Report -->
    <div class="section">
        <h2>Document Overview</h2>
        <div class="stat-grid">
            <div class="stat-box">
                <div class="stat-value">{{ total_pages }}</div>
                <div class="stat-label">Pages</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{{ text_length }}</div>
                <div class="stat-label">Characters</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{{ pattern_count }}</div>
                <div class="stat-label">Pattern Categories</div>
            </div>
        </div>
    </div>

    {% if abuse_patterns %}
    <div class="section">
        <h2>Abuse Patterns Found</h2>
        <table>
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Indicators Found</th>
                </tr>
            </thead>
            <tbody>
            {% for category, keywords in abuse_patterns.items() %}
                <tr>
                    <td><strong>{{ category }}</strong></td>
                    <td>{{ keywords|join(', ') }}</td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
    {% else %}
    <div class="info">
        <p>No specific abuse patterns were detected in this document.</p>
    </div>
    {% endif %}
    {% endif %}

    {% if visualizations %}
    <div class="section">
        <h2>Visualizations</h2>
        {% for viz_type, viz_path in visualizations.items() %}
        <div class="visualization">
            <h3>{{ viz_type|replace('_', ' ')|title }}</h3>
            <img src="{{ viz_path }}" alt="{{ viz_type }}">
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <div class="footer">
        <p><strong>IMPORTANT NOTICE:</strong> This analysis is provided for informational purposes only and should not be considered 
        as professional advice. If you are experiencing abuse or feel unsafe, please contact local authorities or a domestic violence support organization.</p>
        <p>Report generated by <strong>Coercive Control Analyzer</strong></p>
        <p><em>Personal Development</em></p>
    </div>
</body>
</html>
        """

        # Prepare template data
        template_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'filepath': data.get('filepath', 'Unknown'),
            'analysis_type': data.get('analysis_type', 'unknown'),
            'visualizations': visualizations,
            'logo_data': self._get_logo_base64()
        }

        if data.get('analysis_type') == 'conversation_analysis':
            analysis = data.get('analysis', {})
            freq = analysis.get('frequency_patterns', {})
            template_data.update({
                'message_count': freq.get('total_messages', 0),
                'time_span_days': freq.get('time_span', {}).get('duration_days', 'N/A'),
                'abuse_patterns': analysis.get('abuse_patterns', {}),
                'abuse_pattern_count': len(analysis.get('abuse_patterns', {})),
                'escalation_detected': analysis.get('escalation_patterns', {}).get('escalation_detected', False),
                'darvo_tactics': analysis.get('darvo_tactics', {})
            })
        elif data.get('analysis_type') == 'document_analysis':
            template_data.update({
                'total_pages': data.get('total_pages', 0),
                'text_length': data.get('text_length', 0),
                'abuse_patterns': data.get('abuse_patterns', {}),
                'pattern_count': len(data.get('abuse_patterns', {}))
            })

        # Render template
        template = Template(html_template)
        html_content = template.render(**template_data)

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return str(output_path)

    def _generate_json_report(self, data: Dict, output_path: Path) -> str:
        """Generate JSON report."""
        # Add metadata
        report_data = {
            'generated_at': datetime.now().isoformat(),
            'report_version': '1.0',
            'analysis_results': data
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, default=str)

        return str(output_path)

    def _generate_text_report(self, data: Dict, output_path: Path) -> str:
                        # Chronological Timeline of Abuse Trajectory
                        timeline = None
                        if data.get('analysis_type') == 'conversation_analysis':
                            timeline = data.get('analysis', {}).get('timeline', [])
                        elif data.get('analysis_type') == 'document_analysis':
                            timeline = data.get('timeline', [])
                        if timeline:
                            lines.append("\n" + "=" * 80)
                            lines.append("CHRONOLOGICAL TIMELINE OF ABUSE TRAJECTORY (Spine of Report):")
                            lines.append("Each event is listed in order. The user may accept the report as is, or verify each event below.")
                            for event in timeline:
                                lines.append(f"  Time: {event.get('timestamp', '')}  Sender: {event.get('sender', '')}")
                                lines.append(f"    Category: {event.get('category', '')}  Indicator: {event.get('indicator', '')}")
                                lines.append(f"    Message: {event.get('text', '')}")
                                lines.append(f"    Verification: [ ] Accept  [ ] Flag for Review")
                            lines.append(f"Total Timeline Events: {len(timeline)}")
                    def generate_timeline_visualization(self, timeline: list, style: str = 'calendar', output_filename: str = 'timeline.png') -> str:
                        """
                        Generate a timeline visualization in the requested style (calendar, horizontal, vertical).
                        """
                        import matplotlib.pyplot as plt
                        import pandas as pd
                        from pathlib import Path
                        if not timeline:
                            return ""
                        df = pd.DataFrame(timeline)
                        df['timestamp'] = pd.to_datetime(df['timestamp'])
                        # Calendar style (heatmap)
                        if style == 'calendar':
                            df['date'] = df['timestamp'].dt.date
                            date_counts = df.groupby('date').size()
                            fig, ax = plt.subplots(figsize=(12, 6))
                            ax.bar(date_counts.index, date_counts.values, color='red')
                            ax.set_title('Abuse Events Calendar Timeline')
                            ax.set_xlabel('Date')
                            ax.set_ylabel('Number of Events')
                            plt.xticks(rotation=45)
                            plt.tight_layout()
                        elif style == 'horizontal':
                            fig, ax = plt.subplots(figsize=(14, 3))
                            ax.scatter(df['timestamp'], [1]*len(df), c='red', s=50)
                            ax.set_yticks([])
                            ax.set_title('Abuse Events Horizontal Timeline')
                            ax.set_xlabel('Time')
                            plt.tight_layout()
                        elif style == 'vertical':
                            fig, ax = plt.subplots(figsize=(3, 14))
                            ax.scatter([1]*len(df), df['timestamp'], c='red', s=50)
                            ax.set_xticks([])
                            ax.set_title('Abuse Events Vertical Timeline')
                            ax.set_ylabel('Time')
                            plt.tight_layout()
                        else:
                            return ""
                        output_path = Path(self.output_dir) / output_filename
                        plt.savefig(output_path, bbox_inches='tight')
                        plt.close()
                        return str(output_path)
                        # Generate timeline visualizations in all styles
                        timeline = None
                        if analysis_data.get('analysis_type') == 'conversation_analysis':
                            timeline = analysis_data.get('analysis', {}).get('timeline', [])
                        elif analysis_data.get('analysis_type') == 'document_analysis':
                            timeline = analysis_data.get('timeline', [])
                        timeline_viz = {}
                        if timeline:
                            for style in ['calendar', 'horizontal', 'vertical']:
                                fname = f'timeline_{style}.png'
                                path = self.generate_timeline_visualization(timeline, style=style, output_filename=fname)
                                if path:
                                    timeline_viz[style] = path
                # Section for Protective/Reactive Actions
                if data.get('analysis_type') == 'conversation_analysis':
                    protective = data.get('analysis', {}).get('protective_actions', {})
                    if protective:
                        lines.append("\n" + "=" * 80)
                        lines.append("PROTECTIVE/REACTIVE ACTIONS (Not Abuse):")
                        for entry in protective.get('actions', []):
                            lines.append(f"  Time: {entry.get('timestamp', '')}  Sender: {entry.get('sender', '')}")
                            lines.append(f"    Action: {entry.get('action', '')}")
                            lines.append(f"    Context: {entry.get('context', '')}")
                        lines.append(f"Total Protective/Reactive Actions: {len(protective.get('actions', []))}")
                # Add to template_data for HTML report
                if data.get('analysis_type') == 'conversation_analysis':
                    analysis = data.get('analysis', {})
                    template_data['protective_actions'] = analysis.get('protective_actions', {})
                # Add timeline chart for protective/reactive actions if present
                if analysis_data.get('analysis_type') == 'conversation_analysis':
                    analysis = analysis_data.get('analysis', {})
                    protective = analysis.get('protective_actions', {})
                    if protective and protective.get('actions'):
                        path = self.create_timeline_chart(protective['actions'], output_filename='protective_timeline.png')
                        if path:
                            visualizations['protective_timeline'] = path
        """Generate plain text report."""
        lines = []
        lines.append("=" * 80)
        lines.append(" " * 20 + "COERCIVE CONTROL ANALYZER")
        lines.append(" " * 25 + "Personal Development")
        lines.append("=" * 80)
        lines.append("ANALYSIS REPORT")
        lines.append("=" * 80)
        lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"File: {data.get('filepath', 'Unknown')}")
        lines.append(f"Type: {data.get('analysis_type', 'Unknown')}\n")

        if data.get('analysis_type') == 'conversation_analysis':
            lines.append("CONVERSATION ANALYSIS")
            lines.append("-" * 80)
            analysis = data.get('analysis', {})

            # Overview
            freq = analysis.get('frequency_patterns', {})
            lines.append(f"\nTotal Messages: {freq.get('total_messages', 0)}")
            lines.append(f"Time Span: {freq.get('time_span', {}).get('duration_days', 'N/A')} days")

            # DARVO Analysis
            darvo = analysis.get('darvo_tactics', {})
            if darvo:
                lines.append("\n" + "=" * 80)
                lines.append("DARVO TACTICS ANALYSIS")
                lines.append("=" * 80)
                lines.append("\nDARVO is a manipulation tactic involving three steps: Deny, Attack, and Reverse Victim and Offender. Each event is shown below in sequence, with clear explanations.")

                severity = darvo.get('severity_assessment', {})
                if severity:
                    lines.append(f"\nRisk Level: {severity.get('risk_level', 'Unknown').upper()}")
                    lines.append(f"Severity Score: {severity.get('total_score', 0)}")
                    lines.append(f"\n{severity.get('interpretation', '')}")

                forensic = darvo.get('forensic_summary', {})
                if forensic and forensic.get('full_darvo_pattern_detected'):
                    lines.append("\n" + "!" * 80)
                    lines.append("⚠ COMPLETE DARVO PATTERN DETECTED")
                    lines.append("All three components present: Deny, Attack, and Reverse Victim/Offender")
                    lines.append("!" * 80)

                # Child-focused patterns
                child_patterns = darvo.get('child_focused_patterns', {})
                child_total = sum(
                    data.get('count', 0) 
                    for data in child_patterns.values() 
                    if isinstance(data, dict)
                )
                if child_total > 0:
                    lines.append("\n" + "!" * 80)
                    lines.append(f"🚨 HIGH RISK: {child_total} CHILD-FOCUSED MANIPULATION INSTANCES DETECTED")
                    lines.append("!" * 80)

                # Articulate each event pattern in sequence
                lines.append("\n--- DARVO Event Patterns ---")
                deny_patterns = darvo.get('deny_patterns', {})
                attack_patterns = darvo.get('attack_patterns', {})
                reverse_patterns = darvo.get('reverse_patterns', {})

                # DENY
                if deny_patterns:
                    lines.append("\n  1. DENY: The abuser denies the abuse or minimizes responsibility.")
                    for subcat, subdata in deny_patterns.items():
                        if isinstance(subdata, dict) and subdata.get('count', 0) > 0:
                            lines.append(f"    - {subcat.replace('_', ' ').title()}: {subdata['count']} instances")
                            for inst in subdata.get('instances', [])[:3]:
                                lines.append(f"      Example: '{inst.get('text', '')}' (Sender: {inst.get('sender', '')}, Time: {inst.get('timestamp', '')})")

                # ATTACK
                if attack_patterns:
                    lines.append("\n  2. ATTACK: The abuser attacks the victim's credibility, stability, or character.")
                    for subcat, subdata in attack_patterns.items():
                        if isinstance(subdata, dict) and subdata.get('count', 0) > 0:
                            lines.append(f"    - {subcat.replace('_', ' ').title()}: {subdata['count']} instances")
                            for inst in subdata.get('instances', [])[:3]:
                                lines.append(f"      Example: '{inst.get('text', '')}' (Sender: {inst.get('sender', '')}, Time: {inst.get('timestamp', '')})")

                # REVERSE
                if reverse_patterns:
                    lines.append("\n  3. REVERSE VICTIM/OFFENDER: The abuser claims to be the victim and blames the true victim.")
                    for subcat, subdata in reverse_patterns.items():
                        if isinstance(subdata, dict) and subdata.get('count', 0) > 0:
                            lines.append(f"    - {subcat.replace('_', ' ').title()}: {subdata['count']} instances")
                            for inst in subdata.get('instances', [])[:3]:
                                lines.append(f"      Example: '{inst.get('text', '')}' (Sender: {inst.get('sender', '')}, Time: {inst.get('timestamp', '')})")

                # Recommendations
                if forensic and forensic.get('recommended_actions'):
                    lines.append("\nRECOMMENDED ACTIONS:")
                    for action in forensic['recommended_actions']:
                        lines.append(f"  • {action}")

            # Abuse patterns
            abuse = analysis.get('abuse_patterns', {})
            if abuse:
                lines.append("\n" + "-" * 80)
                lines.append("GENERAL ABUSE PATTERNS DETECTED:")
                for category, data_item in abuse.items():
                    lines.append(f"\n  {category}:")
                    lines.append(f"    Occurrences: {data_item.get('count', 0)}")
                    keywords = data_item.get('keywords', [])
                    if keywords:
                        lines.append(f"    Indicators: {', '.join(keywords[:10])}")

            # Escalation
            escalation = analysis.get('escalation_patterns', {})
            if escalation.get('escalation_detected'):
                lines.append("\n" + "!" * 80)
                lines.append("⚠ ESCALATION PATTERN DETECTED")
                lines.append("!" * 80)


        elif data.get('analysis_type') == 'document_analysis':
            lines.append("DOCUMENT ANALYSIS")
            lines.append("-" * 80)
            lines.append(f"\nTotal Pages: {data.get('total_pages', 0)}")
            lines.append(f"Text Length: {data.get('text_length', 0)} characters")

            abuse_patterns = data.get('abuse_patterns', {})
            if abuse_patterns:
                lines.append("\nABUSE PATTERNS FOUND:")
                for category, keywords in abuse_patterns.items():
                    lines.append(f"\n  {category}:")
                    lines.append(f"    Indicators: {', '.join(keywords)}")
                    lines.append(f"    Count: {len(keywords)}")
            else:
                lines.append("\nNo abuse patterns detected.")

        # Escalation Table (for both conversation and document analysis if available)
        escalation = None
        if data.get('analysis_type') == 'conversation_analysis':
            escalation = data.get('analysis', {}).get('escalation_patterns', {})
        elif data.get('analysis_type') == 'document_analysis':
            escalation = data.get('escalation_patterns', {})
        if escalation and escalation.get('details'):
            lines.append("\n" + "=" * 80)
            lines.append("ESCALATION TABLE (Category × Time Window):")
            details = escalation['details']
            # Find max number of windows
            max_windows = max((d.get('windows', 0) for d in details), default=0)
            # Header
            header = ["Category"] + [f"Window {i+1}" for i in range(max_windows)]
            lines.append("\t".join(header))
            # Rows
            for d in details:
                row = [d['category']]
                # Fill in counts for each window (if available)
                window_counts = d.get('window_counts', [])
                for i in range(max_windows):
                    if i < len(window_counts):
                        row.append(str(window_counts[i]))
                    else:
                        row.append("")
                lines.append("\t".join(row))

        lines.append("\n" + "=" * 80)
        lines.append("IMPORTANT NOTICE:")
        lines.append("This analysis is for informational purposes only.")
        lines.append("If you are experiencing abuse, please contact local authorities")
        lines.append("or a domestic violence support organization.")
        lines.append("-" * 80)
        lines.append("Report generated by Coercive Control Analyzer")
        lines.append("Personal Development")
        lines.append("=" * 80)

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        return str(output_path)

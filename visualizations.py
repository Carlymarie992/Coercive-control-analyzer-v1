"""Visualization generation for analysis results."""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime

from config.settings import FIGURE_DPI, FIGURE_SIZE


class AnalysisVisualizations:
    """Generate visualizations for coercive control analysis."""

    def __init__(self, output_dir: str = 'output'):
        """
        Initialize visualization generator.

        Args:
            output_dir: Directory to save visualizations
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = FIGURE_SIZE
        plt.rcParams['figure.dpi'] = FIGURE_DPI

    def create_abuse_pattern_chart(self, abuse_patterns: Dict, output_filename: str = 'abuse_patterns.png') -> str:
        """
        Create bar chart of abuse patterns.

        Args:
            abuse_patterns: Dictionary of abuse patterns
            output_filename: Name for output file

        Returns:
            Path to saved chart
        """
        if not abuse_patterns:
            return ""

        # Prepare data
        categories = list(abuse_patterns.keys())
        counts = [abuse_patterns[cat].get('count', len(abuse_patterns[cat]))
                  if isinstance(abuse_patterns[cat], dict)
                  else len(abuse_patterns[cat])
                  for cat in categories]

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))

        # Create bar chart
        bars = ax.barh(categories, counts, color=sns.color_palette("RdYlGn_r", len(categories)))

        ax.set_xlabel('Number of Indicators Found', fontsize=12)
        ax.set_title('Abuse Pattern Analysis', fontsize=14, fontweight='bold')
        ax.set_xlim(0, max(counts) * 1.1 if counts else 1)

        # Add value labels
        for i, (cat, count) in enumerate(zip(categories, counts)):
            ax.text(count + 0.5, i, str(count), va='center', fontsize=10)

        plt.tight_layout()

        # Save
        output_path = self.output_dir / output_filename
        plt.savefig(output_path, bbox_inches='tight', dpi=FIGURE_DPI)
        plt.close()

        return str(output_path)

    def create_timeline_chart(self, messages: List[Dict], output_filename: str = 'timeline.png') -> str:
        """
        Create timeline chart of messages.

        Args:
            messages: List of message dictionaries
            output_filename: Name for output file

        Returns:
            Path to saved chart
        """
        # Filter messages with timestamps
        timestamped = [m for m in messages if m.get('timestamp')]
        if not timestamped:
            return ""

        # Convert to DataFrame
        df = pd.DataFrame(timestamped)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.normalize()  # type: ignore # Use .normalize() to get date part as datetime64[ns]

        # Count messages per day
        daily_counts = df.groupby('date').size().reset_index(name='count')

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot
        ax.plot(daily_counts['date'], daily_counts['count'], marker='o', linewidth=2)
        ax.fill_between(daily_counts['date'], daily_counts['count'], alpha=0.3)

        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Number of Messages', fontsize=12)
        ax.set_title('Message Frequency Over Time', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)

        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save
        output_path = self.output_dir / output_filename
        plt.savefig(output_path, bbox_inches='tight', dpi=FIGURE_DPI)
        plt.close()

        return str(output_path)

    def create_sender_distribution(self, frequency_data: Dict, output_filename: str = 'sender_distribution.png') -> str:
        """
        Create pie chart of message distribution by sender.

        Args:
            frequency_data: Frequency pattern data
            output_filename: Name for output file

        Returns:
            Path to saved chart
        """
        sender_counts = frequency_data.get('sender_counts', {})
        if not sender_counts:
            return ""

        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))

        # Create pie chart
        colors = sns.color_palette("Set3", len(sender_counts))
        pie_result = ax.pie(
            sender_counts.values(),
            labels=sender_counts.keys(),
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        # Handle both 2-tuple and 3-tuple returns
        if len(pie_result) == 3:
            wedges, texts, autotexts = pie_result
        else:
            wedges, texts = pie_result
            autotexts = []

        # Improve text
        for text in texts:
            text.set_fontsize(12)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)

        ax.set_title('Message Distribution by Sender', fontsize=14, fontweight='bold')

        plt.tight_layout()

        # Save
        output_path = self.output_dir / output_filename
        plt.savefig(output_path, bbox_inches='tight', dpi=FIGURE_DPI)
        plt.close()

        return str(output_path)

    def create_escalation_chart(self, escalation_data: Dict, output_filename: str = 'escalation.png') -> str:
        """
        Create chart showing escalation patterns.

        Args:
            escalation_data: Escalation pattern data
            output_filename: Name for output file

        Returns:
            Path to saved chart
        """
        details = escalation_data.get('details', [])
        if not details:
            return None # type: ignore

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot each category
        for detail in details:
            category = detail['category']
            initial = detail['initial_count']
            final = detail['final_count']
            windows = detail['windows']

            # Simple linear interpolation for visualization
            x = [0, windows - 1]
            y = [initial, final]
            ax.plot(x, y, marker='o', linewidth=2, label=category)

        ax.set_xlabel('Time Window', fontsize=12)
        ax.set_ylabel('Indicator Count', fontsize=12)
        ax.set_title('Escalation Pattern Analysis', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        # Save
        output_path = self.output_dir / output_filename
        plt.savefig(output_path, bbox_inches='tight', dpi=FIGURE_DPI)
        plt.close()

        return str(output_path)

    def generate_all_visualizations(self, analysis_data: Dict) -> Dict[str, str]:
        """
        Generate all applicable visualizations.

        Args:
            analysis_data: Complete analysis data

        Returns:
            Dictionary mapping visualization type to file path
        """
        visualizations = {}

        # Check analysis type
        if analysis_data.get('analysis_type') == 'conversation_analysis':
            analysis = analysis_data.get('analysis', {})

            # Abuse patterns
            abuse_patterns = analysis.get('abuse_patterns', {})
            if abuse_patterns:
                path = self.create_abuse_pattern_chart(abuse_patterns)
                if path:
                    visualizations['abuse_patterns'] = path

            # Frequency patterns
            freq_patterns = analysis.get('frequency_patterns', {})
            if freq_patterns:
                path = self.create_sender_distribution(freq_patterns)
                if path:
                    visualizations['sender_distribution'] = path

            # Escalation
            escalation = analysis.get('escalation_patterns', {})
            if escalation.get('escalation_detected'):
                path = self.create_escalation_chart(escalation)
                if path:
                    visualizations['escalation'] = path

        elif analysis_data.get('analysis_type') == 'document_analysis':
            # Document analysis
            abuse_patterns = analysis_data.get('abuse_patterns', {})
            if abuse_patterns:
                path = self.create_abuse_pattern_chart(abuse_patterns)
                if path:
                    visualizations['abuse_patterns'] = path

        return visualizations

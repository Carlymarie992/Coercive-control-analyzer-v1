"""Application settings and constants for coercive control analysis."""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = os.getenv('DATA_DIR', BASE_DIR / 'data')
OUTPUT_DIR = os.getenv('OUTPUT_DIR', BASE_DIR / 'output')
TEMP_DIR = os.getenv('TEMP_DIR', BASE_DIR / 'temp')

# Analysis settings
DEFAULT_ANALYSIS_THRESHOLD = float(os.getenv('ANALYSIS_THRESHOLD', '0.5'))
MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', '100'))

# Conversation analysis settings
CONVERSATION_TIME_THRESHOLD_MINUTES = int(os.getenv('CONVERSATION_TIME_THRESHOLD', '60'))
ESCALATION_WINDOW_DAYS = int(os.getenv('ESCALATION_WINDOW_DAYS', '7'))

# Report settings
REPORT_FORMATS = ['html', 'json', 'pdf', 'txt']
DEFAULT_REPORT_FORMAT = os.getenv('DEFAULT_REPORT_FORMAT', 'html')

# Visualization settings
FIGURE_DPI = int(os.getenv('FIGURE_DPI', '300'))
FIGURE_SIZE = (12, 8)

# Security settings
ENABLE_ENCRYPTION = os.getenv('ENABLE_ENCRYPTION', 'False').lower() == 'true'
ENABLE_ANONYMIZATION = os.getenv('ENABLE_ANONYMIZATION', 'False').lower() == 'true'

# Logging settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# NLP settings
NLP_MODEL = os.getenv('NLP_MODEL', 'english')
SENTIMENT_POLARITY_THRESHOLD = float(os.getenv('SENTIMENT_POLARITY_THRESHOLD', '-0.1'))

# Supported file formats
SUPPORTED_PDF_EXTENSIONS = ['.pdf']
SUPPORTED_TEXT_EXTENSIONS = ['.txt', '.log', '.chat']
SUPPORTED_JSON_EXTENSIONS = ['.json']
SUPPORTED_CSV_EXTENSIONS = ['.csv']
SUPPORTED_EXTENSIONS = (
    SUPPORTED_PDF_EXTENSIONS +
    SUPPORTED_TEXT_EXTENSIONS +
    SUPPORTED_JSON_EXTENSIONS +
    SUPPORTED_CSV_EXTENSIONS
)

import os
import zipfile
from pathlib import Path
from typing import List

def package_court_ready_zip(selected_files: List[str], output_zip: str, base_dir: str = 'output') -> str:
    """
    Package selected files into a court-ready zip folder structure.

    Args:
        selected_files: List of filenames (relative to base_dir) to include
        output_zip: Path to output zip file
        base_dir: Base directory containing files

    Returns:
        Path to created zip file
    """
    # Define court-ready folder structure
    folder_structure = {
        'Report': [],
        'Visualizations': [],
        'RawData': [],
        'SupportingDocs': []
    }
    # Assign files to folders by extension/type
    for fname in selected_files:
        ext = Path(fname).suffix.lower()
        if ext in ['.html', '.txt', '.pdf']:
            folder_structure['Report'].append(fname)
        elif ext in ['.png', '.jpg', '.jpeg', '.svg']:
            folder_structure['Visualizations'].append(fname)
        elif ext in ['.json', '.csv']:
            folder_structure['RawData'].append(fname)
        else:
            folder_structure['SupportingDocs'].append(fname)
    # Create zip
    zip_path = Path(base_dir) / output_zip
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for folder, files in folder_structure.items():
            for file in files:
                file_path = Path(base_dir) / file
                if file_path.exists():
                    arcname = f"{folder}/{Path(file).name}"
                    zipf.write(file_path, arcname)
    return str(zip_path)

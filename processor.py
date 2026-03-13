import logging
from pathlib import Path
from typing import Iterable



# Finds all files ending in .txt in specified folder and returns them in a list
# NOTE: The paths are returned in no particular order.
def import_files(filepath: Path):
    try:
        files: Iterable[Path] = Path(filepath).glob('*.txt')
        results = []
        for file_path in files:
            text = file_path.read_text(encoding='utf-8')
            results.append((file_path.name, text))
        if results is None or len(results) == 0:
            logging.error(f'No text files found in {filepath}')
            return []
        return results
    except Exception as e:
        logging.error("Import Error: {}".format(e))
        return []
import json
import os
from pathlib import Path
import logging

def read_json_file(file_path):
    logger = logging.getLogger(__name__)

    data_path = Path(file_path)

    if not os.path.exists(data_path):
        logger.warning("No database was found at %s", data_path)
        return []

    with open(data_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if not isinstance(data, list):
                data = []
            return data
        except json.JSONDecodeError:
            logger.error("Database file is corrupted %s", data_path)
            return []

def write_json_file(file_path, data):
    data_path = Path(file_path)
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

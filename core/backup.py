import os
import json
import shutil
from pathlib import Path
import time
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class BackupCreator:
    def __init__(self, data_file=None):
        self.data_file = data_file or os.path.join("database", "data.json")

    def create_backup(self, file_path, store_time, time_index):
        backup_dir = Path.home() / ".cache" / "conf-backup"
        backup_dir.mkdir(parents=True, exist_ok=True)

        file_name = os.path.basename(file_path)
        timestamp = int(time.time())
        backup_file_name = f"{timestamp}_{file_name}.bak"
        backup_path = backup_dir / backup_file_name

        if not os.path.exists(file_path):
            logger.error("File not found: %s", file_path)
            raise FileNotFoundError(f"There is no such file on a given path {file_path}")

        if store_time <= 0:
            logger.error("Invalid store_time: %s", store_time)
            raise ValueError("store_time must be a positive number")

        if time_index == "h":
            delta = timedelta(hours=store_time)
        elif time_index == "d":
            delta = timedelta(days=store_time)
        else:
            logger.error("Invalid index: %s", time_index)
            raise ValueError(f"Incorrect index use -h for hours and -d for days not {time_index}")

        try:
            shutil.copy2(file_path, backup_path)
        except Exception as e:
            logger.exception("Error during copying file")
            raise RuntimeError("Backup failed")

        now_time = datetime.now()
        expire_date = now_time + delta

        new_data = {
            "Original path": file_path,
            "Backup path": str(backup_path),
            "File name": file_name,
            "Expire time": expire_date.isoformat(),
            "ID": int(time.time())
        }

        if not os.path.exists(self.data_file):
            logger.warning("No database was found - created a new one")
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump([], f)

        with open(self.data_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                data = []

        data.append(new_data)

        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        logger.info("Backup created successfully")

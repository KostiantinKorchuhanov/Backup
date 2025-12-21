import os
import json
import shutil
from pathlib import Path
import time
from datetime import datetime, timedelta

class BackupCreator:
    def __init__(self):
        self.data_file = "data.json"

    def create_backup(self, file_path, store_time, time_index):
        backup_dir = Path.home() / ".cache" / "conf-backup"
        backup_dir.mkdir(parents=True, exist_ok=True)

        file_name = os.path.basename(file_path)
        timestamp = int(time.time())
        backup_file_name = f"{timestamp}_{file_name}.bak"
        backup_path = backup_dir / backup_file_name

        if not os.path.exists(file_path):
            raise FileNotFoundError

        if time_index == "h":
            delta = timedelta(hours=store_time)
        elif time_index == "d":
            delta = timedelta(days=store_time)
        else:
            raise ValueError(f"Incorrect index use -h for hours and -d for days")

        try:
            shutil.copy2(file_path, backup_path)
        except Exception as e:
            print(f"Error during copying file: {e}")
            raise FileExistsError

        now_time = datetime.now()
        expire_date = now_time + delta

        new_data = {
            "original_path": file_path,
            "backup_path": backup_path,
            "file_name": file_name,
            "expire_time": expire_date.isoformat(),
            "timestamp": int(time.time())
        }

        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        data.append(new_data)

        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

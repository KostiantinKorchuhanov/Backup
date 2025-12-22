import json
import os
from datetime import datetime

class ClearByTime:
    def __init__(self):
        self.data_file = os.path.join("database", "data.json")

    def check_clean(self):
        with open(self.data_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        now_time = datetime.now()

        new_data = []
        for item in data:
            expire_time = datetime.fromisoformat(item["Expire time"])
            if expire_time > now_time:
                new_data.append(item)
            else:
                backup_path = item.get("Backup path")

                if os.path.exists(backup_path) and os.path.exists(backup_path):
                    os.remove(backup_path)

        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
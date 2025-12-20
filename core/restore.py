import json
import shutil
import os

class RestoreFile:
    def __init__(self, asked_id):
        self.asked_id = asked_id

    def restore_file(self):
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        found_block = None
        for item in data:
            if item["timestamp"] == self.asked_id:
                found_block = item
            else:
                continue

        if not found_block:
            raise ValueError(f"No such file in the backup storage")

        new_data = []
        for item in data:
            if item["timestamp"] != self.asked_id:
                new_data.append(item)
            else:
                continue

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)

        try:
            original_path = found_block.get("original_path")
            backup_path = found_block.get("backup_path")
            shutil.copy2(backup_path, original_path)
        except Exception as e:
            print(f"Error during recovery {e}")

        if os.path.exists(backup_path):
            os.remove(backup_path)


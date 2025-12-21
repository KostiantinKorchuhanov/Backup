import json
import shutil
import os

class RestoreFile:
    def restore_file(self, asked_id):
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        found_block = None
        for item in data:
            if item["timestamp"] == asked_id:
                found_block = item
            else:
                continue

        if not found_block:
            raise ValueError(f"No such file in the backup storage")

        original_path = found_block.get("original_path")
        backup_path = found_block.get("backup_path")
        try:
            shutil.copy2(backup_path, original_path)
        except Exception as e:
            print(f"Error during recovery {e}")

        try:
            new_data = []
            for item in data:
                if item["timestamp"] != asked_id:
                    new_data.append(item)
                else:
                    continue
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error during database changes {e}")

        if os.path.exists(backup_path):
            os.remove(backup_path)


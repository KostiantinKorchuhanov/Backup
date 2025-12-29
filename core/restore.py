import json
import shutil
import os
import logging

logger = logging.getLogger(__name__)

class RestoreFile:
    def __init__(self):
        self.data_file = os.path.join("database", "data.json")

    def restore_file(self, asked_id):
        logger.info("Restoring file started")
        logger.info("Restore requested for ID=%s", asked_id)
        with open(self.data_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        found_block = None
        for item in data:
            if item["ID"] == asked_id:
                found_block = item
            else:
                continue

        if not found_block:
            logger.info("BAD restore requested for ID=%s - check if file exists", asked_id)
            raise ValueError(f"No such file in the backup storage")

        original_path = found_block.get("Original path")
        backup_path = found_block.get("Backup path")
        if not original_path or not backup_path:
            logger.error("Invalid backup entry: %s", found_block)
            raise ValueError("Backup entry is corrupted")
        try:
            shutil.copy2(backup_path, original_path)
            if os.path.exists(backup_path):
                os.remove(backup_path)
        except Exception:
            logger.exception("Error during recovery file with ID=%s", asked_id)
            raise

        try:
            new_data = []
            for item in data:
                if item["ID"] != asked_id:
                    new_data.append(item)
                else:
                    continue
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.exception(f"Error during database changes {e}")
            raise

        logger.info("Finished restoring file")

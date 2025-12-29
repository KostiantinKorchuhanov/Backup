import json
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ClearByTime:
    def __init__(self):
        self.data_file = os.path.join("database", "data.json")

    def check_clean(self):
        logger.info("Cleaner started")
        if not os.path.exists(self.data_file):
            logger.warning("No database found")
            data = []
        else:
            with open(self.data_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
                except json.JSONDecodeError:
                    logger.error("Database file is corrupted, resetting")
                    data = []

        now_time = datetime.now()

        new_data = []
        for item in data:
            try:
                expire_time = datetime.fromisoformat(item["Expire time"])
            except ValueError:
                logger.warning("Invalid expire time in entry: %s", item)
                continue
            if expire_time > now_time:
                new_data.append(item)
            else:
                backup_path = item.get("Backup path")
                if backup_path and os.path.exists(backup_path):
                    try:
                        os.remove(backup_path)
                        logger.info("Backup successfully was removed from: %s", backup_path)
                    except Exception:
                        logger.exception("Error removing backup: %s", backup_path)

        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)

        logger.info("Cleaner ended")
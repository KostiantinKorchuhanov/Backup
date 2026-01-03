import json
import os
from datetime import datetime
import logging

from core.utils import read_json_file, write_json_file

logger = logging.getLogger(__name__)

class ClearByTime:
    def __init__(self):
        self.data_file = os.path.join("database", "data.json")

    def check_clean(self):
        logger.info("Cleaner started")
        data = read_json_file(self.data_file)

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

        write_json_file(self.data_file, new_data)

        logger.info("Cleaner ended")

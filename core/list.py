import json
import os
import logging

logger = logging.getLogger(__name__)

class ShowData:
    def __init__(self):
        self.data_file = os.path.join("database", "data.json")

    def show_data(self):
        logger.info("Showing files started")
        if not os.path.exists(self.data_file):
            logger.warning("No database was found")
            data = []
        else:
            with open(self.data_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
                except json.JSONDecodeError:
                    logger.error("Database file is corrupted")
                    data = []

        for item in data:
            for i, j in item.items():
                print(i, j)
        logger.info("Showing files finished")
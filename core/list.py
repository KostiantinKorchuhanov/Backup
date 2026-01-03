import os
import logging

from core.utils import read_json_file

logger = logging.getLogger(__name__)

class ShowData:
    def __init__(self):
        self.data_file = os.path.join("database", "data.json")

    def show_data(self):
        logger.info("Showing files started")

        data = read_json_file(self.data_file)

        for item in data:
            for i, j in item.items():
                print(i, j)
        logger.info("Showing files finished")
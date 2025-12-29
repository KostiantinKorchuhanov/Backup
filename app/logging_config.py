import os
import logging

logging_file = "app.log"
logging_directory = "logs"

def setup_logging():
    if not os.path.exists(logging_directory):
        os.makedirs(logging_directory)

    logging_path = os.path.join(logging_directory, logging_file)

    logging.basicConfig(level = logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt="%Y-%m-%d %H:%M:%S",
                        handlers=[
                            logging.StreamHandler(),
                            logging.FileHandler(logging_path, encoding="utf-8")
                        ])
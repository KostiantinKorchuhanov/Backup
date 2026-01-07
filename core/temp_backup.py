import logging
import os
import shutil
import time
from pathlib import Path

logger = logging.getLogger(__name__)

class TemporaryBackup:
    def __init__(self, file_path):
        self.file_path = file_path

    def create(self):
        backup_dir = Path.home() / ".cache" / "conf-backup"
        backup_dir.mkdir(parents=True, exist_ok=True)
        file_name = os.path.basename(self.file_path)
        timestamp = int(time.time())
        backup_file_name = f"{timestamp}_{file_name}.bak"
        self.backup_path = backup_dir / backup_file_name

        if not os.path.exists(self.file_path):
            logger.error("File not found: %s", self.file_path)
            raise FileNotFoundError(f"There is no such file on a given path {self.file_path}")

        if not os.path.isfile(self.file_path):
            logger.error("This is not a file: %s", self.file_path)
            raise FileNotFoundError(f"Only files can be backed up, not directories: {self.file_path}")

        try:
            shutil.copy2(self.file_path, self.backup_path)
        except Exception as e:
            logger.exception("Error during copying file")
            raise RuntimeError("Backup failed") from e

    def restore(self):
        if not os.path.exists(self.backup_path):
            logger.error("File not found in backup storage: %s", self.backup_path)
            raise FileNotFoundError(f"There is no such file on a given path {self.backup_path}")

        try:
            shutil.copy2(self.backup_path, self.file_path)
        except Exception as e:
            logger.exception("Error during copying file")
            raise RuntimeError("Backup restoring failed") from e

    def clean(self):
        try:
            if self.backup_path.exists():
                self.backup_path.unlink()
        except Exception:
            logger.exception("Failed to clean temporary backup")
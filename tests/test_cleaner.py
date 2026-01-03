import pytest
import json
from core.backup import BackupCreator
from datetime import datetime,timedelta
from core.cleaner import ClearByTime
import os


@pytest.fixture
def test_data(tmp_path):
    data_file = tmp_path / "data.json"
    test_file = tmp_path / "test.bak"
    test_file.write_text("Arch Linux")

    data = [
        {
            "Backup path": str(test_file),
            "Expire time": (datetime.now() - timedelta(hours=1)).isoformat()
        }
    ]
    data_file.write_text(json.dumps(data))
    return data_file,test_file

def test_remove_expired_data_file(test_data):
    data_file, test_file = test_data
    cleaner = ClearByTime()
    cleaner.data_file = str(data_file)
    cleaner.check_clean()

    assert not test_file.exists()
    with open(data_file) as f:
        data = json.load(f)
    assert data == []

def test_remove_not_expired_data_file(tmp_path):
    data_file = tmp_path / "data.json"
    test_file = tmp_path / "test.bak"
    test_file.write_text("Arch Linux")
    data = [
        {
            "Backup path": str(test_file),
            "Expire time": (datetime.now() + timedelta(hours=1)).isoformat()
        }
    ]
    data_file.write_text(json.dumps(data))
    cleaner = ClearByTime()
    cleaner.data_file = str(data_file)
    cleaner.check_clean()

    assert test_file.exists()
    with open(data_file) as f:
        data = json.load(f)
    assert len(data) == 1

def test_invalid_time(tmp_path):
    data_file = tmp_path / "data.json"
    data = [
        {
            "Expire time": "Incorrect date"
        }
    ]
    cleaner = ClearByTime()
    cleaner.data_file = str(data_file)
    cleaner.check_clean()

    with open(data_file) as f:
        data = json.load(f)
    assert data == []
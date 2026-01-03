from pathlib import Path
import pytest
from core.backup import BackupCreator
import os
import json

def test_create_backup_file_successfully(tmp_path, monkeypatch):
    data_file = tmp_path / "data.json"
    test_file = tmp_path / "test.txt"
    test_file.write_text("Arch Linux")
    backup = BackupCreator(data_file=str(data_file))

    backup_dir = tmp_path / "backup"
    backup_dir.mkdir()
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

    backup.create_backup(file_path=str(test_file), store_time=1, time_index="h")

    assert data_file.exists()

    from core.utils import read_json_file
    data = read_json_file(data_file)
    assert len(data) == 1
    item = data[0]

    assert item["Original path"] == str(test_file)
    assert item["File name"] == "test.txt"
    assert Path(item["Backup path"]).exists()
    assert "ID" in item
    assert isinstance(item["ID"], int)
    assert item["ID"] > 0


def test_file_not_found(tmp_path):
    backup = BackupCreator(data_file=str(tmp_path / "data.json"))
    with pytest.raises(FileNotFoundError):
        backup.create_backup(file_path="sudo_apt_install.txt", store_time=1, time_index="h")


def test_invalid_storage_time(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Arch Linux")
    backup = BackupCreator(data_file=str(tmp_path / "data.json"))
    with pytest.raises(ValueError):
        backup.create_backup(file_path=str(test_file), store_time=0, time_index="h")


def test_invalid_time_index(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Arch Linux")
    backup = BackupCreator(data_file=str(tmp_path / "data.json"))
    with pytest.raises(ValueError):
        backup.create_backup(file_path=str(test_file), store_time=1, time_index="a")
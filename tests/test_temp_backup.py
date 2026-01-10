import pytest
import os
from pathlib import Path
from core.temp_backup import TemporaryBackup


def test_create_temporary_backup(tmp_path, monkeypatch):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Something")

    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

    backup = TemporaryBackup(test_file)
    backup.create()

    assert backup.backup_path.exists()
    assert test_file.read_text() == "Something"

def test_restore_temporary_backup(tmp_path, monkeypatch):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Something")

    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

    backup = TemporaryBackup(test_file)
    backup.create()
    test_file.write_text("NOT Something")

    assert test_file.read_text() == "NOT Something"

    backup.restore()
    assert test_file.read_text() == "Something"

def test_clear_temporary_backup(tmp_path, monkeypatch):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Something")

    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

    backup = TemporaryBackup(test_file)
    backup.create()
    assert backup.backup_path.exists()
    backup.clean()
    assert not backup.backup_path.exists()
    assert test_file.exists()

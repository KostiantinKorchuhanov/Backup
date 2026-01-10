import json
import pytest
from core.restore import RestoreFile

def test_restore_file_successfully(tmp_path, monkeypatch):
    data_file = tmp_path / "data.json"
    backup_file = tmp_path / "backup.txt"
    original_file = tmp_path / "original.txt"
    backup_file.write_text("Something")
    original_file.write_text("NOT Something")

    data = [
        {
            "ID": 314159265,
            "Original path": str(original_file),
            "Backup path": str(backup_file)
        }
    ]
    data_file.write_text(json.dumps(data))
    restore = RestoreFile()
    monkeypatch.setattr(restore, "data_file", str(data_file))
    restore.restore_file(314159265)

    assert original_file.read_text() == "Something"
    assert not backup_file.exists()

    updated_data = json.loads(data_file.read_text())
    assert updated_data == []


def test_restore_file_not_found(tmp_path, monkeypatch):
    data_file = tmp_path / "data.json"
    data_file.write_text("[]")
    restore = RestoreFile()
    monkeypatch.setattr(restore, "data_file", str(data_file))

    with pytest.raises(ValueError, match="No such file"):
        restore.restore_file(562951413)

def test_restore_file_entry_corrupted(tmp_path, monkeypatch):
    data_file = tmp_path / "data.json"
    data = [
        {
            "ID": 314159265,
            "Original path": None,
            "Backup path": None
        }
    ]
    data_file.write_text(json.dumps(data))

    restore = RestoreFile()
    monkeypatch.setattr(restore, "data_file", str(data_file))

    with pytest.raises(ValueError, match="corrupted"):
        restore.restore_file(314159265)


def test_restore_file_backup_error(tmp_path, monkeypatch):
    data_file = tmp_path / "data.json"
    data = [
        {
            "ID": 314159265,
            "Original path": "/no",
            "Backup path": "/still/no"
        }
    ]
    data_file.write_text(json.dumps(data))

    def fake_file_copy(*args, **kwargs):
        raise OSError("K-boom")

    restore = RestoreFile()
    monkeypatch.setattr(restore, "data_file", str(data_file))
    monkeypatch.setattr("shutil.copy2", fake_file_copy)

    with pytest.raises(OSError):
        restore.restore_file(314159265)


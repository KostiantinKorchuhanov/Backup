import pytest
import json
from core.list import ShowData


@pytest.fixture
def test_data(tmp_path):
    data_file = tmp_path / "data.json"
    return data_file

def test_show_data_no_file(tmp_path, capsys):
    show = ShowData()
    show.data_file = str(tmp_path / "some.json")
    show.show_data()
    listed_output = capsys.readouterr()
    assert listed_output.out == ""

def test_show_correct_data(test_data, capsys):
    data = [
        {
            "Original path": "/some/original/path",
            "Backup path": "/some/backup/path",
            "File name": "test.txt",
            "Expire time": "2025-12-12",
            "ID": "314159265"
        }
    ]
    test_data.write_text(json.dumps(data))
    show = ShowData()
    show.data_file = str(test_data)
    show.show_data()
    listed_output = capsys.readouterr().out

    assert "Original path /some/original/path" in listed_output
    assert "Backup path /some/backup/path" in listed_output
    assert "File name test.txt" in listed_output
    assert "Expire time 2025-12-12" in listed_output
    assert "ID 314159265" in listed_output

def test_show_broken_data_file(test_data, capsys):
    test_data.write_text("{some incorrect data}")
    show = ShowData()
    show.data_file = str(test_data)
    show.show_data()
    listed_output = capsys.readouterr()
    assert listed_output.out == ""
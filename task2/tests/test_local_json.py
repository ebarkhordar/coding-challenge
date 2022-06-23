import json
from pathlib import Path

from my_data_store.api import JsonRecord


def test_insert_records(tmp_path):
    f1 = tmp_path / "data"
    f1.mkdir()
    file_path = f1.joinpath(Path('example.json'))
    storage = JsonRecord(file_path)
    sample_data = {
        "id": 1,
        "name": "first",
        "score": 1.0,
    }
    storage.insert(record=sample_data)
    with open(file_path, 'r') as file:
        json_data = json.loads(file.read())
        assert json_data == [sample_data]
    sample_data_2 = {
        "id": 2,
        "name": "second",
        "score": 2.0,
    }
    sample_data_3 = {
        "id": 3,
        "name": "third",
        "score": 3.0,
    }
    storage.batch_insert(batch_records=[sample_data_2, sample_data_3])
    with open(file_path, 'r') as file:
        json_data = json.loads(file.read())
        assert len(json_data) == 3
        assert json_data == [sample_data, sample_data_2, sample_data_3]


def test_query_record(tmp_path):
    f1 = tmp_path / "data"
    f1.mkdir()
    file_path = f1.joinpath(Path('example.json'))
    storage = JsonRecord(file_path)
    sample_data_2 = {
        "id": 2,
        "name": "second",
        "score": 2.0,
    }
    sample_data_3 = {
        "id": 3,
        "name": "third",
        "score": 3.0,
    }
    with open(file_path, 'w') as file:
        json_data = json.dumps([sample_data_2, sample_data_3])
        file.write(json_data)
    record = storage.get_record_by_id(record_id=3)
    assert record == sample_data_3

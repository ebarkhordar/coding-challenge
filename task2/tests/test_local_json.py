import json
from pathlib import Path

import pytest

from my_data_store.api import JsonRecord


@pytest.fixture
def json_record(tmp_path):
    f1 = tmp_path / "data"
    f1.mkdir()
    file_path = f1.joinpath(Path('example.json'))
    json_record = JsonRecord(file_path)
    return json_record


def test_insert(json_record):
    sample_data = {
        "id": 1,
        "name": "first",
        "score": 1.0,
    }
    json_record.insert(record=sample_data)
    with open(json_record.file_path, 'r') as file:
        json_data = json.loads(file.read())
        assert json_data == [sample_data]
        assert len(json_data) == 1


def test_batch_insert(json_record):
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
    json_record.batch_insert(batch_records=[sample_data_2, sample_data_3])
    with open(json_record.file_path, 'r') as file:
        json_data = json.loads(file.read())
        assert json_data == [sample_data_2, sample_data_3]
        assert len(json_data) == 3


def test_query_record(json_record):
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
    with open(json_record.file_path, 'w') as file:
        json_data = json.dumps([sample_data_2, sample_data_3])
        file.write(json_data)
    record = json_record.get_record_by_id(record_id=3)
    assert record == sample_data_3


def test_query_records_with_filters(json_record):
    sample_data_1 = {
        "id": 1,
        "name": "first",
        "color": "red",
        "city": "Hong Kong",
        "score": 1.0,
    }
    sample_data_2 = {
        "id": 2,
        "name": "second",
        "color": "red",
        "city": "Paris",
        "score": 2.0,
    }
    sample_data_3 = {
        "id": 3,
        "name": "third",
        "color": "orange",
        "city": "Paris",
        "score": 3.0,
    }
    sample_data_4 = {
        "id": 4,
        "name": "third",
        "color": "black",
        "city": "Bangkok",
        "score": 4.0,
    }

    with open(json_record.file_path, 'w') as file:
        json_data = json.dumps([sample_data_1, sample_data_2, sample_data_3, sample_data_4])
        file.write(json_data)
    record = json_record.get_record_with_filter(color='red')
    assert record == [sample_data_1, sample_data_2]

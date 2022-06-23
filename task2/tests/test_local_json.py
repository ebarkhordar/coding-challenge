import json
from pathlib import Path

import pytest

from my_data_store.api import JsonRecord

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


@pytest.fixture
def json_record(tmp_path):
    f1 = tmp_path / "data"
    f1.mkdir()
    file_path = f1.joinpath(Path('example.json'))
    json_record = JsonRecord(file_path)
    return json_record


def test_insert(json_record):
    json_record.insert(record=sample_data_1)
    with open(json_record.file_path, 'r') as file:
        json_data = json.loads(file.read())
        assert json_data == [sample_data_1]
        assert len(json_data) == 1


def test_batch_insert(json_record):
    json_record.batch_insert(batch_records=[sample_data_1, sample_data_2])
    with open(json_record.file_path, 'r') as file:
        json_data = json.loads(file.read())
        assert json_data == [sample_data_1, sample_data_2]
        assert len(json_data) == 2


def test_query_record(json_record):
    with open(json_record.file_path, 'w') as file:
        json_data = json.dumps([sample_data_2, sample_data_3])
        file.write(json_data)
    record = json_record.get_record_by_id(record_id=3)
    assert record == sample_data_3
    record = json_record.get_record_by_id(record_id=31)
    assert record == "No record has found!"


def test_query_records_with_filters(json_record):
    with open(json_record.file_path, 'w') as file:
        json_data = json.dumps([sample_data_1, sample_data_2, sample_data_3, sample_data_4])
        file.write(json_data)
    records = json_record.get_record_with_filter(color='red')
    assert records == [sample_data_1, sample_data_2]


def test_query_records_with_filters_offset_and_limit(json_record):
    data_list = []
    for i in range(1, 100):
        record = {
            "id": i,
        }
        if i % 3 == 0:
            record['color'] = 'red'
        elif i % 3 == 1:
            record['color'] = 'orange'
        elif i % 3 == 2:
            record['color'] = 'blue'
        data_list.append(record)
    with open(json_record.file_path, 'w') as file:
        json_data = json.dumps(data_list)
        file.write(json_data)
    records = json_record.get_record_with_filter(limit=10, color='red')
    assert len(records) == 10
    records = json_record.get_record_with_filter(limit=2, offset=1, color='orange')
    assert records == [{'id': 4, 'color': 'orange'}, {'id': 7, 'color': 'orange'}]


def test_update_record_by_id(json_record):
    with open(json_record.file_path, 'w') as file:
        json_data = json.dumps([sample_data_1, sample_data_2, sample_data_3, sample_data_4])
        file.write(json_data)
    record = json_record.update_record_by_id(record_id=4, color='pink', city='Tehran')
    updated_sample_data_4 = {
        "id": 4,
        "name": "third",
        "color": "pink",
        "city": "Tehran",
        "score": 4.0,
    }
    assert record == updated_sample_data_4
    with open(json_record.file_path, 'r') as file:
        json_data = json.loads(file.read())
        assert json_data == [sample_data_1, sample_data_2, sample_data_3, updated_sample_data_4]
        assert len(json_data) == 4


def test_delete_record_by_id(json_record):
    with open(json_record.file_path, 'w') as file:
        json_data = json.dumps([sample_data_1, sample_data_2, sample_data_3, sample_data_4])
        file.write(json_data)
    message = json_record.delete_record_by_id(record_id=3)
    assert message == "Record has been deleted successfully"
    with open(json_record.file_path, 'r') as file:
        json_data = json.loads(file.read())
        assert json_data == [sample_data_1, sample_data_2, sample_data_4]
        assert len(json_data) == 3

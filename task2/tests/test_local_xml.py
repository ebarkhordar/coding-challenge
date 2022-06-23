from pathlib import Path

import pytest
from dicttoxml import dicttoxml

from my_data_store.api import XMLRecord
from my_data_store.utils import xml_to_json_records

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
xml_sample_data_1 = """<?xml version="1.0" encoding="UTF-8" ?>
<root>
    <item type="dict">
        <id type="int">1</id>
        <name type="str">first</name>
        <color type="str">red</color>
        <city type="str">Hong Kong</city>
        <score type="float">1.0</score>
    </item>
</root>"""


@pytest.fixture
def xml_record(tmp_path):
    f1 = tmp_path / "data"
    f1.mkdir()
    file_path = f1.joinpath(Path('example.xml'))
    xml_record = XMLRecord(file_path)
    return xml_record


def test_insert(xml_record):
    xml_record.insert(record=sample_data_1)
    with open(xml_record.file_path, "r") as f:
        xml_string = f.read()
        records = xml_to_json_records(xml_string)
        assert records == [sample_data_1]


def test_batch_insert(xml_record):
    xml_record.batch_insert(batch_records=[sample_data_1, sample_data_2])
    with open(xml_record.file_path, "r") as f:
        xml_string = f.read()
        records = xml_to_json_records(xml_string)
        assert records == [sample_data_1, sample_data_2]


def test_query_record(xml_record):
    with open(xml_record.file_path, 'wb') as file:
        xml_data = dicttoxml([sample_data_1, sample_data_2])
        file.write(xml_data)
    record = xml_record.get_record_by_id(record_id=2)
    assert record == sample_data_2
    record = xml_record.get_record_by_id(record_id=31)
    assert record == "No record has found!"


def test_query_records_with_filters(xml_record):
    with open(xml_record.file_path, 'wb') as file:
        xml_data = dicttoxml([sample_data_1, sample_data_2, sample_data_3, sample_data_4])
        file.write(xml_data)
    records = xml_record.get_record_with_filter(color='red')
    assert records == [sample_data_1, sample_data_2]


def test_query_records_with_filters_offset_and_limit(xml_record):
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
    with open(xml_record.file_path, 'wb') as file:
        xml_data = dicttoxml(data_list)
        file.write(xml_data)
    records = xml_record.get_record_with_filter(limit=10, color='red')
    assert len(records) == 10
    records = xml_record.get_record_with_filter(limit=2, offset=1, color='orange')
    assert records == [{'id': 4, 'color': 'orange'}, {'id': 7, 'color': 'orange'}]


def test_update_record_by_id(xml_record):
    with open(xml_record.file_path, 'wb') as file:
        xml_data = dicttoxml([sample_data_1, sample_data_2, sample_data_3, sample_data_4])
        file.write(xml_data)
    record = xml_record.update_record_by_id(record_id=4, color='pink', city='Tehran')
    updated_sample_data_4 = {
        "id": 4,
        "name": "third",
        "color": "pink",
        "city": "Tehran",
        "score": 4.0,
    }
    assert record == updated_sample_data_4
    with open(xml_record.file_path, "r") as f:
        xml_string = f.read()
        records = xml_to_json_records(xml_string)
        assert records == [sample_data_1, sample_data_2, sample_data_3, updated_sample_data_4]
        assert len(records) == 4


def test_delete_record_by_id(xml_record):
    with open(xml_record.file_path, 'wb') as file:
        xml_data = dicttoxml([sample_data_1, sample_data_2, sample_data_3, sample_data_4])
        file.write(xml_data)
    message = xml_record.delete_record_by_id(record_id=3)
    assert message == "Record has been deleted successfully"
    with open(xml_record.file_path, "r") as f:
        xml_string = f.read()
        records = xml_to_json_records(xml_string)
        assert records == [sample_data_1, sample_data_2, sample_data_4]
        assert len(records) == 3

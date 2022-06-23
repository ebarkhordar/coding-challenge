import io
import json
from ftplib import FTP

import pytest
from my_data_store.api import JsonRecord, FTPHandler
from my_data_store.settings import Settings
from my_data_store.utils import dict_to_binary, Reader

ftp_conf = (Settings.FTP_HOSTNAME, Settings.FTP_USERNAME, Settings.FTP_PASSWORD)
ftp = FTP(*ftp_conf)

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
    json_record = JsonRecord('example.json', FTPHandler)
    return json_record


def read_file_ftp(file_path):
    r = Reader()
    ftp.retrbinary(f'RETR {file_path}', r)
    res_binary = r.data
    res = res_binary.decode()
    return res


def test_insert(json_record):
    ftp.delete(json_record.file_path)
    json_record.insert(record=sample_data_1)
    res = read_file_ftp(json_record.file_path)
    json_data = json.loads(res)
    assert json_data == [sample_data_1]
    assert len(json_data) == 1


def test_batch_insert(json_record):
    ftp.delete(json_record.file_path)
    json_record.batch_insert(batch_records=[sample_data_1, sample_data_2])
    res = read_file_ftp(json_record.file_path)
    json_data = json.loads(res)
    assert json_data == [sample_data_1, sample_data_2]
    assert len(json_data) == 2


def test_query_record(json_record):
    records_binary = dict_to_binary([sample_data_2, sample_data_3])
    ftp.storbinary(f"STOR {json_record.file_path}", io.BufferedReader(io.BytesIO(records_binary)))
    record = json_record.get_record_by_id(record_id=3)
    assert record == sample_data_3
    record = json_record.get_record_by_id(record_id=31)
    assert record == "No record has found!"


def test_query_records_with_filters(json_record):
    records_binary = dict_to_binary([sample_data_1, sample_data_2, sample_data_3, sample_data_4])
    ftp.storbinary(f"STOR {json_record.file_path}", io.BufferedReader(io.BytesIO(records_binary)))
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
    records_binary = dict_to_binary(data_list)
    ftp.storbinary(f"STOR {json_record.file_path}", io.BufferedReader(io.BytesIO(records_binary)))
    records = json_record.get_record_with_filter(limit=10, color='red')
    assert len(records) == 10
    records = json_record.get_record_with_filter(limit=2, offset=1, color='orange')
    assert records == [{'id': 4, 'color': 'orange'}, {'id': 7, 'color': 'orange'}]


def test_update_record_by_id(json_record):
    records_binary = dict_to_binary([sample_data_1, sample_data_2, sample_data_3, sample_data_4])
    ftp.storbinary(f"STOR {json_record.file_path}", io.BufferedReader(io.BytesIO(records_binary)))
    record = json_record.update_record_by_id(record_id=4, color='pink', city='Tehran')
    updated_sample_data_4 = {
        "id": 4,
        "name": "third",
        "color": "pink",
        "city": "Tehran",
        "score": 4.0,
    }
    assert record == updated_sample_data_4
    res = read_file_ftp(json_record.file_path)
    json_data = json.loads(res)
    assert json_data == [sample_data_1, sample_data_2, sample_data_3, updated_sample_data_4]
    assert len(json_data) == 4


def test_delete_record_by_id(json_record):
    records_binary = dict_to_binary([sample_data_1, sample_data_2, sample_data_3, sample_data_4])
    ftp.storbinary(f"STOR {json_record.file_path}", io.BufferedReader(io.BytesIO(records_binary)))
    message = json_record.delete_record_by_id(record_id=3)
    assert message == "Record has been deleted successfully"
    res = read_file_ftp(json_record.file_path)
    json_data = json.loads(res)
    assert json_data == [sample_data_1, sample_data_2, sample_data_4]
    assert len(json_data) == 3

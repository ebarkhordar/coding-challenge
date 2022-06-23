import json
from pathlib import Path
from threading import Lock
from typing import List
from dicttoxml import dicttoxml

from my_data_store.utils import dict_to_binary, sampling, xml_to_json_records


class JsonRecord:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.lock = Lock()

    def get_all_records(self):
        if self.file_path.is_file():
            with open(self.file_path, "rb") as f:
                json_binary = f.read()
                json_string = json_binary.decode()
                records = json.loads(json_string)
                return records
        return []

    def insert(self, record: dict):
        with self.lock:
            records = self.get_all_records()
            records.append(record)
            records_binary = dict_to_binary(records)
            with open(self.file_path, "wb") as f:
                f.write(records_binary)

    def batch_insert(self, batch_records: List[dict]):
        with self.lock:
            records = self.get_all_records()
            records.extend(batch_records)
            records_binary = dict_to_binary(records)
            with open(self.file_path, "wb") as f:
                f.write(records_binary)

    def get_record_by_id(self, record_id):
        records = self.get_all_records()
        for record in records:
            if record['id'] == record_id:
                return record
        return "No record has found!"

    def get_record_with_filter(self, limit=5, offset=0, **kwargs):
        records = self.get_all_records()
        selected_records = []
        for record in records:
            for k, v in kwargs.items():
                if record[k] == v:
                    selected_records.append(record)
        return sampling(selected_records, offset, limit)

    def sync_records_with_file(self, records):
        records_binary = dict_to_binary(records)
        with open(self.file_path, "wb") as f:
            f.write(records_binary)

    def update_record_by_id(self, record_id, **kwargs):
        with self.lock:
            records = self.get_all_records()
            for record in records:
                if record['id'] == record_id:
                    for k, v in kwargs.items():
                        record[k] = v
                    self.sync_records_with_file(records)
                    return record
            return "No record has found!"

    def delete_record_by_id(self, record_id):
        with self.lock:
            records = self.get_all_records()
            for record in records:
                if record['id'] == record_id:
                    records.remove(record)
                    self.sync_records_with_file(records)
                    return "Record has been deleted successfully"
            return "No record has found!"


class XMLRecord:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.lock = Lock()

    def get_all_records(self):
        if self.file_path.is_file():
            with open(self.file_path, "rb") as f:
                xml_binary = f.read()
                xml_string = xml_binary.decode()
                records = xml_to_json_records(xml_string)
                return records
        return []

    def insert(self, record: dict):
        with self.lock:
            records = self.get_all_records()
            records.append(record)
            records_binary = dicttoxml(records)
            with open(self.file_path, "wb") as f:
                f.write(records_binary)

    def batch_insert(self, batch_records: List[dict]):
        with self.lock:
            records = self.get_all_records()
            records.extend(batch_records)
            records_binary = dicttoxml(records)
            with open(self.file_path, "wb") as f:
                f.write(records_binary)

    def get_record_by_id(self, record_id):
        records = self.get_all_records()
        for record in records:
            if record['id'] == record_id:
                return record
        return "No record has found!"

    def get_record_with_filter(self, limit=5, offset=0, **kwargs):
        records = self.get_all_records()
        selected_records = []
        for record in records:
            for k, v in kwargs.items():
                if record[k] == v:
                    selected_records.append(record)
        return sampling(selected_records, offset, limit)

    def sync_records_with_file(self, records):
        records_binary = dicttoxml(records)
        with open(self.file_path, "wb") as f:
            f.write(records_binary)

    def update_record_by_id(self, record_id, **kwargs):
        with self.lock:
            records = self.get_all_records()
            for record in records:
                if record['id'] == record_id:
                    for k, v in kwargs.items():
                        record[k] = v
                    self.sync_records_with_file(records)
                    return record
            return "No record has found!"

    def delete_record_by_id(self, record_id):
        with self.lock:
            records = self.get_all_records()
            for record in records:
                if record['id'] == record_id:
                    records.remove(record)
                    self.sync_records_with_file(records)
                    return "Record has been deleted successfully"
            return "No record has found!"

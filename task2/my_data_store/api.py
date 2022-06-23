import json
from pathlib import Path
from typing import List

from my_data_store.utils import dict_to_binary
from threading import Lock


class JsonRecord:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.lock = Lock()

    def insert(self, record: dict):
        records = self.get_all_records()
        records.append(record)
        records_binary = dict_to_binary(records)
        with self.lock:
            with open(self.file_path, "wb") as f:
                f.write(records_binary)

    def batch_insert(self, batch_records: List[dict]):
        records = self.get_all_records()
        records.extend(batch_records)
        records_binary = dict_to_binary(records)
        with self.lock:
            with open(self.file_path, "wb") as f:
                f.write(records_binary)

    def get_all_records(self):
        if self.file_path.is_file():
            with open(self.file_path, "rb") as f:
                json_binary = f.read()
                json_string = json_binary.decode()
                records = json.loads(json_string)
                return records
        return []

    def get_record_by_id(self, record_id):
        records = self.get_all_records()
        for record in records:
            if record['id'] == record_id:
                return record
        return "No record has found!"

    def get_record_with_filter(self, **kwargs):
        records = self.get_all_records()
        selected_records = []
        for record in records:
            for k, v in kwargs.items():
                if record[k] == v:
                    selected_records.append(record)
        return selected_records

    def update_record_by_id(self, record_id, **kwargs):
        records = self.get_all_records()
        for record in records:
            if record['id'] == record_id:
                for k, v in kwargs.items():
                    record[k] = v
                return record
        return "No record has found!"

    def delete_record_by_id(self, record_id):
        with open(self.file_path, "rb") as f:
            json_file = f.read()
            records = self.get_all_records(json_file)
            return records.delete(record_id)

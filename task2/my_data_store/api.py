import io
import json
from ftplib import FTP
from pathlib import Path
from threading import Lock
from typing import List, Union
from dicttoxml import dicttoxml

from my_data_store.settings import Settings
from my_data_store.utils import dict_to_binary, sampling, xml_to_json_records, Reader


class FTPHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.ftp_conf = (Settings.FTP_HOSTNAME, Settings.FTP_USERNAME, Settings.FTP_PASSWORD)
        self.ftp = FTP(*self.ftp_conf)

    def read_binary(self):
        r = Reader()
        self.ftp.retrbinary(f'RETR {self.file_path}', r)
        res_binary = r.data
        return res_binary

    def write_binary(self, data: bytes):
        self.ftp.storbinary(f"STOR {self.file_path}", io.BufferedReader(io.BytesIO(data)))

    def check_file_exists(self):
        return self.file_path in self.ftp.nlst()[0]


class LocalHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_binary(self):
        with open(self.file_path, "rb") as f:
            return f.read()

    def write_binary(self, data: bytes):
        with open(self.file_path, "wb") as f:
            f.write(data)

    def check_file_exists(self):
        return self.file_path.is_file()


class JsonRecord:
    def __init__(self, file_path: Union[Path, str], handler):
        self.file_path = file_path
        self.handler = handler(self.file_path)
        self.lock = Lock()

    def get_all_records(self):
        if self.handler.check_file_exists():
            json_binary = self.handler.read_binary()
            json_string = json_binary.decode()
            records = json.loads(json_string)
            return records
        return []

    def insert(self, record: dict):
        if isinstance(record, list):
            raise Exception("Use batch insertion for more than one record")
        with self.lock:
            records = self.get_all_records()
            records.append(record)
            records_binary = dict_to_binary(records)
            self.handler.write_binary(records_binary)

    def batch_insert(self, batch_records: List[dict]):
        with self.lock:
            records = self.get_all_records()
            records.extend(batch_records)
            records_binary = dict_to_binary(records)
            self.handler.write_binary(records_binary)

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
        self.handler.write_binary(records_binary)

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
    def __init__(self, file_path: Union[Path, str], handler):
        self.file_path = file_path
        self.handler = handler(self.file_path)
        self.lock = Lock()

    def get_all_records(self):
        if self.handler.check_file_exists():
            xml_binary = self.handler.read_binary()
            xml_string = xml_binary.decode()
            records = xml_to_json_records(xml_string)
            return records
        return []

    def insert(self, record: dict):
        if isinstance(record, list):
            raise Exception("Use batch insertion for more than one record")
        with self.lock:
            records = self.get_all_records()
            records.append(record)
            records_binary = dicttoxml(records)
            self.handler.write_binary(records_binary)

    def batch_insert(self, batch_records: List[dict]):
        with self.lock:
            records = self.get_all_records()
            records.extend(batch_records)
            records_binary = dicttoxml(records)
            self.handler.write_binary(records_binary)

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
        self.handler.write_binary(records_binary)

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

import io
from ftplib import FTP
from pathlib import Path
import json
import dicttoxml
from threading import Lock

from my_data_store.settings import Settings


def dict_to_binary(the_dict):
    str = json.dumps(the_dict)
    return str.encode()


class InsertRecord:
    def __init__(self, data, file_format, destination):
        self.data = data
        self.file_format = file_format
        self.destination = destination
        self.lock = Lock()

    def save(self):
        data, mode, file_name = self.get_file()
        if self.destination == 'local drive':
            with self.lock:
                with open(file_name, "wb") as f:
                    f.write(data)
        elif self.destination == 'ftp':
            ftp_conf = (Settings.FTP_HOSTNAME, Settings.FTP_USERNAME, Settings.FTP_PASSWORD)
            with FTP(*ftp_conf) as ftp:
                ftp.storbinary(f"STOR {file_name}", io.BufferedReader(io.BytesIO(data)))

    def get_file(self):
        if self.file_format == 'json':
            return dict_to_binary(self.data), 'a+', 'file.json'
        elif self.file_format == 'xml':
            return dicttoxml.dicttoxml(self.data), 'wb', 'file.xml'
        elif self.file_format == 'binary':
            return dict_to_binary(self.data), 'wb', 'file.bin'


    def get_last_json_data(self, file_path):
        with open(file_path, "r") as jsonFile:
            data = json.load(jsonFile)
            return data

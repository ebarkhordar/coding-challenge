import io
import ftplib
import json
import dicttoxml
from threading import Lock

from my_data_store.settings import Settings


class InsertRecord:
    def __init__(self, data, file_format, destination):
        self.data = data
        self.file_format = file_format
        self.destination = destination
        self.lock = Lock()

    def save(self):
        data, mode, file_name = self.get_file()
        if self.destination == 'local drive':
            self.save_json(data, file_name, file_name)
        elif self.destination == 'ftp':
            session = ftplib.FTP(Settings.FTP_HOSTNAME, user=Settings.FTP_USERNAME, passwd=Settings.FTP_PASSWORD)
            file = open(file_name, 'rb')  # file to send
            session.storbinary('STOR kitten.json', file)  # send the file
            file.close()  # close file and FTP
            session.quit()

    def get_file(self):
        if self.file_format == 'json':
            return self.data, 'a+', 'file.json'
        elif self.file_format == 'xml':
            return dicttoxml.dicttoxml(self.data), 'wb', 'file.xml'
        elif self.file_format == 'binary':
            bite_array = ' '.join(format(ch, 'b') for ch in bytearray(self.data))
            return bite_array, 'wb', 'file.bin'

    def save_json(self, new_data, input_address, output_address):
        with self.lock:
            data = self.get_last_json_data(input_address)

            data.append(new_data)

            with open(output_address, "w") as jsonFile:
                json.dump(data, jsonFile)

    def get_last_json_data(self, file_path):
        with open(file_path, "r") as jsonFile:
            data = json.load(jsonFile)
            return data

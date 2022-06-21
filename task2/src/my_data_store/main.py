import json
from dataclasses import dataclass
import dicttoxml

from my_data_store.settings import Settings


@dataclass
class CustomDataStructure:
    name: str
    value: float
    count: int = 0


class InsertRecord:
    def __init__(self, data, file_format, destination):
        self.data = data
        self.file_format = file_format
        self.destination = destination

    def save(self):
        data, file_name = self.get_file()
        if self.destination == 'local':
            file = open(file_name, 'wb')
            file.write(data)
            file.close()
        elif self.destination == 'ftp':
            pass

    def get_file(self):
        if self.file_format == 'json':
            return json.dumps(self.data), 'file.json'
        elif self.file_format == 'xml':
            return dicttoxml.dicttoxml(self.data), 'file.xml'
        elif self.file_format == 'binary':
            bite_array = ' '.join(format(ch, 'b') for ch in bytearray(self.data))
            return bite_array, 'file.bin'

# class BaseFile:
#     def __int__(self, data):
#         self.data = data
#
#     def get(self):
#         pass
#
#
# class JsonFile(BaseFile):
#     def __int__(self, data):
#         self.data = data
#
#     def get(self):
#         return self.data
#
#
# class XMLFile(BaseFile):
#     def __int__(self, data):
#         self.data = data
#
#     def get(self):
#         return dicttoxml.dicttoxml(self.data)

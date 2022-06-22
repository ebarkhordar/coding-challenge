from my_data_store.api import InsertRecord
from my_data_store.settings import Settings


def test_insert_data():
    sample_data = {
        "name": "test",
        "count": 12,
        "version": 8.2,
    }
    for file_format in Settings.SUPPORTED_FORMATS:
        for destination in Settings.SUPPORTED_DESTINATIONS:
            storage = InsertRecord(
                data=sample_data,
                file_format=file_format,
                destination=destination,
            )
            storage.save()

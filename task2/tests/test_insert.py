from my_data_store.api import InsertRecord


def test_insert_data():
    sample_data = {
        "name": "test",
        "count": 12,
        "version": 8.2,
    }
    storage = InsertRecord(
        data=sample_data,
        file_format="json",
        destination="ftp",
    )
    storage.save()

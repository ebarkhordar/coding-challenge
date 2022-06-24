# My date store

## What is for?

It is a library to store records(dict objects) in multiple file formats and destinations.

* The exposed API is thread-safe.

* Every supported storage format can be combined with any of the supported storage destinations.

* Current supported formats: `Json`, `XML `

* Current supported destinations: `Local drive`, `FTP `

## examples:

Insert a json record:

```
json_record = JsonRecord('simple.json', LocalHandler)
sample_data = {
    "id": 1,
    "name": "first",
    "color": "red",
    "city": "Hong Kong",
    "score": 1.0,
}
json_record.insert(record=sample_data)
```
_Tip1: If you want to use FTP destination, just replace `LocalHandler` with `FTPHandler` in the code above._ 

_Tip2: If you want to save records in XML format, just replace `JsonRecord` with `XMLRecord` in the code above._ 

Batch insert records:

```
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
json_record.batch_insert(batch_records=[sample_data_2, sample_data_3])
```

Retrieve a json record:

```
record = json_record.get_record_by_id(record_id=1)
```

Retrieve json records with filters:

```
records = json_record.get_record_with_filter(color='red')
```

Retrieve json records with filters:

```
records = json_record.get_record_with_filter(color='red')
records = json_record.get_record_with_filter(limit=2, offset=1, color='orange')
```

Update a json record by id:

```
record = json_record.update_record_by_id(record_id=4, color='pink', city='Tehran')
```

Delete a json record by id:

```
message = json_record.delete_record_by_id(record_id=3)
```
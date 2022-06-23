import json
from itertools import islice


def dict_to_binary(the_dict) -> bytes:
    string = json.dumps(the_dict, indent=4, sort_keys=True)
    return string.encode()


def sampling(selection, offset=0, limit=None):
    return list(islice(islice(selection, offset, None), limit))

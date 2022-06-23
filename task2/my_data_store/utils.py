import json


def dict_to_binary(the_dict) -> bytes:
    string = json.dumps(the_dict, indent=4, sort_keys=True)
    return string.encode()

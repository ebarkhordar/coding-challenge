import json
import xmltodict
from itertools import islice


def dict_to_binary(the_dict) -> bytes:
    string = json.dumps(the_dict, indent=4, sort_keys=True)
    return string.encode()


def sampling(selection, offset=0, limit=None):
    return list(islice(islice(selection, offset, None), limit))


def xml_to_json_records(xml_string):
    parsed = xmltodict.parse(xml_string)
    dict_items = []
    if isinstance(parsed['root']['item'], dict):
        return [parse_item(parsed['root']['item'])]
    for item in parsed['root']['item']:
        s_dict = parse_item(item)
        dict_items.append(s_dict)
    return dict_items


def parse_item(item):
    s_dict = {}
    for key, value in item.items():
        if key[0] == '@':
            continue
        else:
            key_type = eval(value['@type'])
            s_dict[key] = key_type(value['#text'])
    return s_dict

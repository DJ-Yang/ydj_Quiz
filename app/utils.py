import json

def convert_list_to_str(data: list):
    return json.dumps(data)

def convert_str_to_list(data: str):
    return json.loads(data)
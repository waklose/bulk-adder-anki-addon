#read json
import json
import os

def read_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

current_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_dir, 'config.json')
data = read_json(config_file_path)
source_field = data['source_field']
target_field = data['target_field']
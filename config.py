#read json
import json
import os

def read_json(file):
    with open(file, 'r', encoding="utf-8") as f:
        data = json.load(f)
    return data

current_dir = os.path.dirname(os.path.abspath(__file__))

config_file_path = os.path.join(current_dir, 'config.json')
config_data = read_json(config_file_path)
source_field = config_data['source_field']
target_field = config_data['target_field']

dict_file_path = os.path.join(current_dir, 'kanji_dictionary.json')
dict_data = read_json(dict_file_path)
full_kanji_dictionary = {entry[0]: entry for entry in dict_data}

dict_file_path_2 = os.path.join(current_dir, 'kanji_dictionary_2.json')
dict_data_2 = read_json(dict_file_path_2)
for i in dict_data_2:
    full_kanji_dictionary[i[0]] = i

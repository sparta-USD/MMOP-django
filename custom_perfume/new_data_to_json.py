import csv
import json


def update_notes_json_files(csv_file_name, json_file_name):
    with open(csv_file_name, newline='', encoding='utf-8') as csvfile, open(json_file_name, newline='', encoding='utf-8') as jsonfile:
        csv_reader = csv.DictReader(csvfile)
        json_reader = json.load(jsonfile)
        
        for row in csv_reader:
            obj_pk = int(row['id']) - 1
            json_reader[obj_pk]['fields'].update({'tag': row['tag']})
            json_reader[obj_pk]['fields'].update({'kor_name': row['new_kor_name']})
        
        with open(json_file_name, 'w', newline='', encoding='utf-8') as f:
            json.dump(json_reader, f, indent=4, ensure_ascii=False)

csv_file = "data/MMOP_Reducing_Custom_perfume_note.csv"
json_file = "data/notes.json"

# update_notes_json_files(csv_file, json_file)


# src/data_manager.py
import csv
import os

def load_dictionary_fields(csv_path):
    """Reads the master dictionary CSV to get the list of fields (first column)."""
    fields = []
    try:
        with open(csv_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            if 'CAMPO' not in reader.fieldnames:
                 f.seek(0)
                 reader = csv.DictReader(f, delimiter=',')

            if 'CAMPO' not in reader.fieldnames:
                 raise ValueError(f"Column 'CAMPO' not found in {csv_path}. Found: {reader.fieldnames}")
            
            for row in reader:
                if row['CAMPO'].strip():
                    fields.append(row['CAMPO'].strip())
    except Exception as e:
        print(f"Error reading dictionary {csv_path}: {e}")
        return []
    return fields

def initialize_csv(output_path, fields):
    """Initializes the output CSV with headers."""
    try:
        with open(output_path, mode='w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields, delimiter=';')
            writer.writeheader()
        return True
    except IOError as e:
        print(f"Error initializing CSV: {e}")
        return False

def append_to_csv(output_path, fields, data):
    """Appends a single row of data to the CSV."""
    try:
        with open(output_path, mode='a', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields, delimiter=';')
            writer.writerow(data)
    except IOError as e:
        print(f"Error writing to CSV: {e}")

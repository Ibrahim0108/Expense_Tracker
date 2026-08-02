import os
from pathlib import Path
from utils.helpers import load_json_file, write_json_file_atomic

BASE_DIR = Path(__file__).resolve().parents[1]
DB_DIR = BASE_DIR / "db"
DB_DIR.mkdir(exist_ok=True)
DATA_FILE = DB_DIR / "data.json"



def ensure_datafile():
    if not DATA_FILE.exists():
        write_json_file_atomic(str(DATA_FILE))

def read_data():
    ensure_datafile()
    data = load_json_file(str(DATA_FILE))
    if data is None:
        write_json_file_atomic(str(DATA_FILE), data)
    return data

def write_data(data):
    write_json_file_atomic(str(DATA_FILE), data)
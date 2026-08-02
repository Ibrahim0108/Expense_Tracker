
import json, os, threading
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "db", "data.json")

def read_json():
    if not os.path.exists(DB_FILE):
        # Initialize empty JSON if file doesn't exist
        with open(DB_FILE, "w") as f:
            json.dump({"settings": {"pin_hash": None}, "users": {}}, f, indent=4)
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Reset JSON if corrupted
            return {"settings": {"pin_hash": None}, "users": {}}


def write_json(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def ensure_user_skeleton(username):
    data = read_json()
    if username not in data["users"]:
        # New user skeleton
        data["users"][username] = {
            "join_date": datetime.now().strftime("%Y-%m-%d"),
            "monthly_data": {},
            "all_time_savings": 0,
            "last_rollover_month": None,
        }
        write_json(data)
    return data["users"][username]

def ensure_month_skeleton(username, month):
    user = ensure_user_skeleton(username)
    if month not in user["monthly_data"]:
        user["monthly_data"][month] = {
            "income": [],
            "expenses": [],
            "lendings": [],
            "deductions": {"total": 0, "paid": 0},
            "savings": 0
        }
        data = read_json()
        data["users"][username] = user
        write_json(data)
    return user["monthly_data"][month]

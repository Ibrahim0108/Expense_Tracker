import os
import json
from werkzeug.security import generate_password_hash, check_password_hash

def hash_pin(pin: str) -> str:
    return generate_password_hash(pin)

def verify_pin_hash(pin: str, pin_hash: str) -> bool:
    return check_password_hash(pin_hash, pin)

def load_json_file(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return {}  # empty file → empty dict
            return json.loads(content)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"WARNING: JSON decode failed for {path}, returning empty dict")
        return {}

    
def write_json_file_atomic(path: str, data):
    # atomic write: write to temp file then rename
    import tempfile
    dirn = os.path.dirname(path) or "."
    fd, tmp = tempfile.mkstemp(dir=dirn)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)
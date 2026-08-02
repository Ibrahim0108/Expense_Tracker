from flask import Blueprint, request, jsonify, current_app, session
from pathlib import Path
import os
import json
from services.data_service import read_data, write_data
from services.lock_service import lock_acquire, lock_release, lock_status
from services.site_attempt_blocker import register_attempt, is_blocked
from utils.helpers import verify_pin_hash


bp = Blueprint("pin", __name__, url_prefix="/api/pin")

# session key for server session-stored flag (flask session)
PIN_SESSION_KEY = "pin_ok"

def get_pin_hash_from_env_or_file():
    # 1. Check env variable first
    env_hash = os.environ.get("SECRET_PIN_HASH")
    if env_hash:
        return env_hash

    # 2. Check secrets file (robust path)
    import sys
    secrets_path = Path(__file__).resolve().parent.parent / "secrets" / "secret.json"
    print("DEBUG secrets_path:", secrets_path)
    if secrets_path.is_file():
        try:
            with open(secrets_path, "r", encoding="utf-8") as f:
                d = json.load(f)
            pin_hash = d.get("pin_hash")
            if not pin_hash:
                raise ValueError("No pin_hash found in secret.json")
            return pin_hash
        except Exception as e:
            print("Error reading secret.json:", e)
            return None

    # 3. Fall back to data.json
    data = read_data()
    return data.get("settings", {}).get("pin_hash")


@bp.route("/verify", methods=["POST"])
def verify_pin():
    body = request.get_json() or {}

    pin = body.get("pin", "")
    if not pin:
        return jsonify({"ok": False, "error": "pin required"}), 400
    

    blocked, secs_left = is_blocked()
    if blocked:
        return jsonify({"ok": False, "error": f"blocked. Try again in {secs_left//60} min"}), 403
    
    pin_hash = get_pin_hash_from_env_or_file()
    if not pin_hash:
        return jsonify({"ok": False, "error": "no_pin_configured"}), 500
    
    if verify_pin_hash(pin, pin_hash):
        register_attempt(success=True)
        # set session flag and acquire global app lock for single-user mode
        session[PIN_SESSION_KEY] = True
        # lock for 1 hour (3600s) or use env override
        import os
        duration = int(os.environ.get("PIN_SESSION_SECONDS", "3600"))
        lock_acquire(duration)
        return jsonify({"ok": True})
    else:
        register_attempt(success=False)
        return jsonify({"ok": False, "error": "invalid_pin"}), 401
    

@bp.route("/status", methods=["GET"])
def status():
    s = lock_status()
    pin_session = bool(session.get(PIN_SESSION_KEY, False))
    return jsonify({"ok": True, "pin_session": pin_session, "lock": s})


@bp.route("/logout", methods=["POST"])
def logout():
    # clear session and release lock
    session.pop(PIN_SESSION_KEY, None)
    lock_release()
    return jsonify({"ok": True})
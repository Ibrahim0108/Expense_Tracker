from flask import Blueprint, request, jsonify
from utils.file_handler import ensure_user_skeleton, read_json
from services.transaction_service import handle_month_rollover

user_bp = Blueprint("user_bp", __name__, url_prefix="/api")

@user_bp.route("/login", methods=["POST"])
def login():
    body = request.get_json() or {}
    username = body.get("username")

    if not username:
        return jsonify({"error": "Username required"}), 400
    handle_month_rollover(username)
    user_data = ensure_user_skeleton(username)
    return jsonify({"status": "success", "user": user_data}), 200

@user_bp.route("/get-user/<username>", methods=["GET"])
def get_user(username):
    data = read_json()
    user_data = data.get("users", {}).get(username)
    if not user_data:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"status": "success", "user": user_data}), 200


@user_bp.route("/find_by_join_date", methods=["GET"])
def find_by_join_date():
    """
    Query param: join_date
    Returns username if found, else 404
    """
    join_date = request.args.get("join_date")
    if not join_date:
        return jsonify({"ok": False, "error": "join_date required"}), 400

    data = read_json()  # or read_data() if that’s your function
    users = data.get("users", {})

    for username, user_data in users.items():
        if user_data.get("join_date") == join_date:
            return jsonify({"ok": True, "username": username}), 200

    return jsonify({"ok": False, "error": "User not found"}), 404

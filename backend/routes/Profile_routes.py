from flask import Blueprint, request, jsonify
from utils.file_handler import read_json

# Blueprint
profile_bp = Blueprint("profile_bp", __name__, url_prefix="/api/profile")


@profile_bp.route("/get", methods=["GET"])
def get_profile():
    """
    Returns user profile details + summary of all-time savings.
    Query param: ?username=<username>
    """
    username = request.args.get("username")
    if not username:
        return jsonify({"ok": False, "error": "username required"}), 400

    data = read_json()
    user = data.get("users", {}).get(username)
    if not user:
        return jsonify({"ok": False, "error": "user not found"}), 404
    
    all_time_savings = user.get("all_time_savings", 0)

    # profile info
    profile_info = {
        "username": username,
        "join_date": user.get("join_date"),
        "all_time_savings": all_time_savings,
    }

    # return both profile info and full monthly data (for history)
    return jsonify({
        "ok": True,
        "profile": profile_info,
        "history": user.get("monthly_data", {})
    }), 200



@profile_bp.route("/get_history", methods=["GET"])
def get_history():
    """
    Returns only user's month-wise history.
    Query param: ?username=<username>
    """
    username = request.args.get("username")
    if not username:
        return jsonify({"ok": False, "error": "username required"}), 400

    data = read_json()
    user = data.get("users", {}).get(username)
    if not user:
        return jsonify({"ok": False, "error": "user not found"}), 404

    months = user.get("monthly_data", {})
    return jsonify({"ok": True, "history": months}), 200

from flask import Blueprint, request, jsonify
from utils.file_handler import read_json

history_bp = Blueprint("history_bp", __name__, url_prefix="/api/history")

@history_bp.route("/month", methods=["GET"])
def get_history_month():
    username = request.args.get("username")
    year = request.args.get("year")
    month = request.args.get("month")

    if not username or not year or not month:
        return jsonify({"error": "username, year, month required"}), 400

    data = read_json()
    user = data["users"].get(username)

    if not user:
        return jsonify({"error": "User not found"}), 404

    month_key = f"{year}-{str(month).zfill(2)}"

    month_data = user["monthly_data"].get(month_key)

    if not month_data:
        return jsonify({"exists": False})

    # -----------------------------
    # BUILD CLEAN RESPONSE
    # -----------------------------
    response = {
        "exists": True,
        "income": month_data.get("income_base", 0),
        "savings": month_data.get("savings", 0),
        "expenses": month_data.get("expenses", [])
    }

    return jsonify(response), 200
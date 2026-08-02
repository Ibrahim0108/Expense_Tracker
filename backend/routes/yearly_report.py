from flask import Blueprint, request, jsonify
from utils.file_handler import read_json,write_json
from datetime import datetime

yearly_bp = Blueprint("yearly_bp", __name__, url_prefix="/api/report")

@yearly_bp.route("/yearly", methods=["GET"])
def get_yearly_report():
    username = request.args.get("username")
    year = request.args.get("year")

    if not username or not year:
        return jsonify({"ok": False, "error": "username and year required"}), 400

    data = read_json()
    user = data["users"].get(username)
    if not user:
        return jsonify({"ok": False, "error": "User not found"}), 404

    monthly_data = user.get("monthly_data", {})

    total_income = 0
    total_savings = 0
    total_lent = 0
    total_returned = 0

    yearly_expenses = []
    yearly_lendings = []

    for month_key, month_value in monthly_data.items():
        if not month_key.startswith(year):
            continue
        
        # Income
        for inc in month_value.get("income", []):
            total_income += inc["amount"]

        # Savings
        total_savings += month_value.get("savings", 0)

        # Expenses (table)
        for exp in month_value.get("expenses", []):
            yearly_expenses.append(exp)

        # Lending (table)
        for lend in month_value.get("lendings", []):
            yearly_lendings.append(lend)
            total_lent += lend["amount"]
            if lend.get("returned"):
                total_returned += lend["amount"]

    return jsonify({
        "ok": True,
        "username": username,
        "year": year,
        "summary": {
            "total_income": total_income,
            "total_savings": total_savings,
            "total_lent": total_lent,
            "total_returned": total_returned
        },
        "expenses": yearly_expenses,
        "lendings": yearly_lendings
    }), 200


@yearly_bp.route("/yearly", methods=["DELETE"])
def delete_yearly_report():
    username = request.json.get("username")
    year = request.json.get("year")

    if not username or not year:
        return jsonify({"ok": False, "error": "username and year required"}), 400

    data = read_json()
    user = data["users"].get(username)
    if not user:
        return jsonify({"ok": False, "error": "User not found"}), 404

    monthly_data = user.get("monthly_data", {})
    months_to_delete = [k for k in monthly_data if k.startswith(year)]
    for m in months_to_delete:
        del monthly_data[m]

    user["monthly_data"] = monthly_data
    write_json(data)

    return jsonify({"ok": True, "message": f"All data for {year} deleted"}), 200


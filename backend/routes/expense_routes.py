from flask import Blueprint, request, jsonify
from services.transaction_service import add_expense, edit_expense, delete_expense

expense_bp = Blueprint("expense_bp", __name__, url_prefix="/api/expense")

@expense_bp.route("/add-expense", methods=["POST"])
def route_add_expense():
    body = request.get_json() or {}
    username = body.get("username")
    amount = body.get("amount")
    category = body.get("category")

    if not username or not amount or not category:
        return jsonify({"ok": False, "error": "username, amount, and category required"}), 400

    res = add_expense(username, amount, category)
    return jsonify(res), 200


@expense_bp.route("/edit", methods=["POST"])
def route_edit_expense():
    body = request.get_json() or {}
    username = body.get("username")
    index = body.get("index")
    amount = body.get("amount")
    category = body.get("category")

    if username is None or index is None:
        return jsonify({"ok": False, "error": "username and index required"}), 400

    res = edit_expense(username, int(index), amount, category)
    return jsonify(res), 200

@expense_bp.route("/delete",methods=["POST"])
def route_delete_expense():
    body = request.get_json() or {}
    username = body.get("username")
    index = body.get("index")

    if username is None or index is None:
        return jsonify({"ok": False, "error": "username and index required"}), 400
    
    res = delete_expense(username ,int(index))
    return jsonify(res), 200


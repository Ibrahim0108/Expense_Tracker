# routes/deduction_routes.py
from flask import Blueprint, request, jsonify
from services.deduction_service import pay_deduction

deduction_bp = Blueprint("deduction_bp", __name__, url_prefix="/api/deduction")

@deduction_bp.route("/pay", methods=["POST"])
def route_pay_deduction():
    body = request.get_json() or {}
    username = body.get("username")
    amount = body.get("amount")
    
    if not username or amount is None:
        return jsonify({"ok": False, "error": "Missing User or amount"}), 400
    
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError()
    except:
        return jsonify({"ok": False, "error": "Invalid amount"}), 400
    
    res = pay_deduction(username, amount)
    if res.get("ok"):
        return jsonify(res), 200
    else:
        return jsonify(res), 400

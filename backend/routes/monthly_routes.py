from flask import Blueprint, request, jsonify
from datetime import datetime
from services.data_service import read_data, write_data  
from utils.file_handler import read_json, write_json, ensure_month_skeleton, ensure_user_skeleton

monthly_bp = Blueprint("monthly_bp", __name__, url_prefix="/api/monthly")

def current_month_key():
    return datetime.now().strftime("%Y-%m")

@monthly_bp.route("/check",methods=["GET"])
def check_month():
    """
    Query params: username
    Returns { new_month: true/false, month: "YYYY-MM", month_data: {...} or null }
    """
    username = request.args.get("username")
    if not username:
        return jsonify({"ok": False, "error": "username required"}), 400
    
    data = read_json()
    user = data.get("users", {}).get(username)
    month = current_month_key()

    # if user doesn't exist -> create skeleton and mark new_month True
    if not user:
        user = ensure_user_skeleton(username)
        return jsonify({"ok": True, "new_month": True, "month": month, "month_data": None}), 200
    
    monthly_data = user.get("monthly_data", {})
    if month not in monthly_data:
        return jsonify({"ok": True, "new_month": True, "month": month, "month_data": None}), 200
    
    # month exists
    return jsonify({"ok": True, "new_month": False, "month": month, "month_data": monthly_data.get(month)}), 200



@monthly_bp.route("/setup", methods=["POST"])
def setup_month():
    """
    Body: { username, income }
    Creates/updates the current month skeleton and sets income & deduction
    """
    body = request.get_json() or {}
    username = body.get("username")
    income = body.get("income")
    category = body.get("category", "General")
    enable_deduction = body.get("enable_deduction", False)

    if not username or income is None:
        return jsonify({"ok": False, "error": "username and income required"}), 400
    
    try:
        income = float(income)
    except Exception:
        return jsonify({"ok": False, "error": "income must be numeric"}), 400
    
    month = current_month_key()

    data = read_json()
    # ensure user and month skeleton exist
    ensure_user_skeleton(username)
    month_data = ensure_month_skeleton(username, month)


    income_entry = {
        "category": category,
        "amount": income,
        "datetime": datetime.now().strftime("%Y-%m-%d || %I:%M %p")
    }
    month_data["income"].append(income_entry)

    # set income (we'll store as a single number for the month-level base income)
    month_data["income_base"] = month_data.get("income_base", 0) + income  # base income for the month
    month_data["deduction_enabled"] = enable_deduction
    # set deductions structure if missing
    ded_total = round((income * 2.5) / 100, 2)  # 2.5%
    if enable_deduction:
        ded_total = round(month_data["income_base"] * 0.025, 2)
        month_data["deductions"] = {
            "total": ded_total,
            "paid": month_data["deductions"].get("paid", 0),
            "remaining": round(ded_total - month_data["deductions"].get("paid", 0), 2)
        }
        month_data["savings"] = round(month_data["income_base"] - ded_total, 2)
    else:
        # No deduction applied
        month_data["deductions"] = {
            "total": 0,
            "paid": 0,
            "remaining": 0
        }
        month_data["savings"] = month_data["income_base"]


    data = read_json()  # reload to ensure we have latest
    data["users"][username]["monthly_data"][month] = month_data
    write_json(data)

    return jsonify({
        "ok": True,
        "month": month,
        "month_data": month_data
    }), 200



@monthly_bp.route("/get", methods=["GET"])
def get_month():
    """
    Query params: username
    Returns month data for current month
    """
    username = request.args.get("username")
    if not username:
        return jsonify({"ok": False, "error": "username required"}), 400
    
    month = current_month_key()
    data = read_json()
    user = data.get("users", {}).get(username)
    if not user:
        return jsonify({"ok": False, "error": "user not found"}), 404
    
    month_data = user.get("monthly_data", {}).get(month)
    if not month_data:
        return jsonify({"ok": True, "month": month, "month_data": None}), 200
    
    # compute remaining deduction (total - paid) and ensure keys exist
    ded = month_data.get("deductions", {"total": 0, "paid": 0})
    ded_total = ded.get("total", 0)
    ded_paid = ded.get("paid", 0)
    remaining = ded_total - ded_paid
    month_data["deductions"]["remaining"] = remaining
    

    return jsonify({"ok": True, "month": month, "month_data": month_data}), 200


@monthly_bp.route("/toggle_deduction", methods=["POST"])
def toggle_deduction():
    """
    Body: { username, enable_deduction }
    Enables/disables deduction for current month
    """
    body = request.get_json() or {}
    username = body.get("username")
    enable_deduction = body.get("enable_deduction", False)

    if not username:
        return jsonify({"ok": False, "error": "username required"}), 400

    month = current_month_key()
    data = read_json()
    user = data["users"].get(username)
    if not user:
        return jsonify({"ok": False, "error": "user not found"}), 404

    month_data = user["monthly_data"].get(month)
    if not month_data:
        return jsonify({"ok": False, "error": "month not found"}), 404

    # Toggle it
    month_data["deduction_enabled"] = enable_deduction

    if enable_deduction:
        ded_total = round(month_data["income_base"] * 0.025, 2)
        month_data["deductions"]["total"] = ded_total
        month_data["deductions"]["remaining"] = ded_total - month_data["deductions"].get("paid", 0)
    else:
        month_data["deductions"] = {"total": 0, "paid": 0, "remaining": 0}


        # === Recalculate savings ===
    total_expenses = sum(e["amount"] for e in month_data.get("expenses", []))
    total_lendings = sum(l["amount"] for l in month_data.get("lendings", []) if not l.get("returned", False))
    total_deduction_paid = month_data["deductions"].get("paid", 0)

    month_data["savings"] = round(
        month_data["income_base"] - total_expenses - total_lendings - total_deduction_paid, 2
    )

    write_json(data)

    return jsonify({"ok": True, "deduction_enabled": enable_deduction, "month_data": month_data}), 200

    


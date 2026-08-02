from flask import Blueprint,jsonify,request
from datetime import datetime
from utils.file_handler import read_json,write_json,ensure_month_skeleton

lending_bp = Blueprint("lending_bp",__name__,url_prefix="/api/lending")

@lending_bp.route("/add", methods=["POST"])
def add_lending():
    body = request.get_json() or {}
    username = body.get("username")
    amount = body.get("amount")
    to_whom = body.get("to_whom")
    reason = body.get("reason")

    if not username or not amount or not to_whom:
        return jsonify({"ok":False ,"error":"Missing Fields"}), 400
    
    month = datetime.now().strftime("%Y-%m")
    data = read_json()
    month_data = ensure_month_skeleton(username, month)

    amount = float(amount)
    current_savings = float(month_data.get("savings", 0))

    if amount > current_savings:
        return jsonify({
            "ok": False,
            "error": f"Not enough savings. Available: {current_savings}"
        }), 400
    

    entry = {
        "amount": amount,
        "to_whom": to_whom,
        "reason": reason,
        "date": datetime.now().strftime("%Y-%m-%d || %I:%M %p"),
        "returned": False
    }

    month_data.setdefault("lendings", []).append(entry)
    # reduce available amount since lent
    month_data["savings"] = max(current_savings - amount, 0)

    data["users"][username]["monthly_data"][month] = month_data
    write_json(data)
    return jsonify({"ok": True, "lending": entry, "month_data": month_data})


@lending_bp.route("/mark-returned",methods = ["POST"])
def mark_returned():
    body = request.get_json() or {}
    username = body.get("username")
    to_whom = body.get("to_whom")
    

    if not username or not to_whom:
        return jsonify({"ok": False, "error": "Missing fields"}), 400
    
    
    month = datetime.now().strftime("%Y-%m")
    data = read_json()
    month_data = ensure_month_skeleton(username, month)
 
    found = False
    for lending in month_data.get("lendings", []):
        if lending["to_whom"] == to_whom and not lending["returned"]:
            lending["returned"] = True
            # add back to available
            month_data["savings"] += lending["amount"]
            break

    if not found:
        return jsonify({"ok": False, "error": "No pending lending found"}), 404
    

    data["users"][username]["monthly_data"][month] = month_data
    write_json(data)
    return jsonify({"ok": True, "month_data": month_data})


@lending_bp.route("/get/<username>", methods=["GET"])
def get_lendings(username):
    month = datetime.now().strftime("%Y-%m")
    data = read_json()
    month_data = ensure_month_skeleton(username, month)

    return jsonify({
        "ok": True,
        "lendings": month_data.get("lendings", []),
        "savings": month_data.get("savings", 0)
    })

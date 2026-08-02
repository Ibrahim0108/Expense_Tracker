# services/deduction_service.py
from utils.file_handler import read_json, write_json
from datetime import datetime

def pay_deduction(username, amount):
    data = read_json()
    # find user by join_date
    user = data["users"].get(username)
    if not user:
        return {"ok": False, "error": "User not found"}
    
    month = datetime.now().strftime("%Y-%m")
    month_data = user["monthly_data"].get(month)
    if not month_data:
        return {"ok": False, "error": "Month data not found"}
    
    if "deductions" not in month_data or month_data["deductions"].get("total", 0) == 0:
        return {"ok": False, "error": "Deduction total not set for this month"}
    
    month_data["deductions"]["paid"] = month_data["deductions"].get("paid", 0) + amount
    month_data["deductions"]["remaining"] = max(month_data["deductions"]["total"] - month_data["deductions"]["paid"], 0)
    
    # save back
    data["users"][username]["monthly_data"][month] = month_data
    write_json(data)
    
    return {"ok": True, "month_data": month_data}

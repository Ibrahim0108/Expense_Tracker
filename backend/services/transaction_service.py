from datetime import datetime
from utils.file_handler import read_json, write_json, ensure_month_skeleton

def add_expense(username, amount, category):
    month = datetime.now().strftime("%Y-%m")  # current month
    month_data = ensure_month_skeleton(username, month)

    current_savings = month_data.get("savings", 0)

    # ❌ Block adding expense greater than savings
    if amount > current_savings:
        return {
            "ok": False,
            "error": f"Expense cannot be greater than remaining savings ({current_savings})"
        }

    entry = {
        "amount": amount,
        "category": category,
        "datetime": datetime.now().strftime("%Y-%m-%d || %I:%M %p")
    }

    month_data["expenses"].append(entry)
    
    # update savings after expenses
    total_expenses = sum(e["amount"] for e in month_data["expenses"])
    month_data["savings"] = month_data.get("income_base", 0) - total_expenses



    # save back
    data = read_json()
    data["users"][username]["monthly_data"][month] = month_data
    write_json(data)

    return {"ok": True, "month_data": month_data, "message": "Expense added"}

def delete_expense(username, index):
    month = datetime.now().strftime("%Y-%m")
    data = read_json()
    user = data["users"].get(username)
    if not user:
        return {"ok": False, "error": "User not found"}

    month_data = user["monthly_data"].get(month)
    if not month_data or index >= len(month_data["expenses"]):
        return {"ok": False, "error": "Invalid index"}

    del month_data["expenses"][index]

    total_expenses = sum(e["amount"] for e in month_data["expenses"])
    month_data["savings"] = max(0, month_data["income_base"] - total_expenses)


    write_json(data)

    return {"ok": True, "month_data": month_data, "message": "Expense deleted"}


def edit_expense(username, index, amount, category):
    month = datetime.now().strftime("%Y-%m")
    data = read_json()
    user = data["users"].get(username)
    if not user:
        return {"ok": False, "error": "User not found"}

    month_data = user["monthly_data"].get(month)
    if not month_data or index >= len(month_data["expenses"]):
        return {"ok": False, "error": "Invalid index"}

    expense = month_data["expenses"][index]

    # update values
    if amount is not None:
        expense["amount"] = amount
    if category:
        expense["category"] = category

    # adjust savings accordingly
    total_expenses = sum(e["amount"] for e in month_data["expenses"])
    month_data["savings"] = max(0, month_data["income_base"] - total_expenses)

    # only add "updated_at" for edit tracking
    expense["updated_at"] = datetime.now().strftime("%Y-%m-%d || %I:%M %p")

    write_json(data)
    return {"ok": True, "month_data": month_data, "message": "Expense updated"}


def handle_month_rollover(username):
    data = read_json()
    user = data["users"].get(username)
    if not user:
        return

    current_month = datetime.now().strftime("%Y-%m")
    months = sorted(user["monthly_data"].keys())

    last_rolled = user.get("last_rollover_month")

    # Find only past months
    past_months = [m for m in months if m < current_month]
    if not past_months:
        return
    
    last_month = past_months[-1]

    if last_rolled == last_month:
        return
    
    last_data = user["monthly_data"][last_month]

     # Add last month's savings
    last_savings = last_data.get("savings", 0)

    user["all_time_savings"] += last_savings

    user["last_rollover_month"] = last_month

    # Create current month skeleton if missing
    if current_month not in user["monthly_data"]:
        from utils.file_handler import ensure_month_skeleton
        ensure_month_skeleton(username, current_month)

    write_json(data)


    



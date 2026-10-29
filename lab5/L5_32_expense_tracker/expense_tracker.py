"""Track monthly expenses and demonstrate basic budget reporting."""

import hmac
import os
import tempfile
import webbrowser
from datetime import datetime
from pathlib import Path


expenses = []
budget_state = {"monthly_budget": 20000}
REPORT_DIR = Path(tempfile.gettempdir()) / "expense_reports"


def add_expense(amount, category="Misc", note=""):
    """Record a positive expense and report whether it was accepted."""
    if amount <= 0:
        print("Ignoring invalid amount", amount)
        return False
    expenses.append({
        "amount": amount,
        "category": category,
        "note": note,
        "time": datetime.now().isoformat(),
    })
    return True


def total_by_category():
    """Return the total spending grouped by category."""
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return totals


def set_budget(new_budget):
    """Set the monthly spending budget."""
    budget_state["monthly_budget"] = new_budget


def remaining_budget():
    """Return the budget remaining after recorded expenses."""
    spent = sum(expense["amount"] for expense in expenses)
    return budget_state["monthly_budget"] - spent


def biggest_expense():
    """Return the largest recorded expense, or None when there are none."""
    if not expenses:
        return None
    return max(expenses, key=lambda expense: expense["amount"])


def print_ledger():
    """Print each expense in the order it was recorded."""
    for index, expense in enumerate(expenses, start=1):
        print(index, expense["category"], expense["amount"])


def check_sync_password(password):
    """Check a password supplied through the BANK_SYNC_PASSWORD setting."""
    expected_password = os.environ.get("BANK_SYNC_PASSWORD")
    if not expected_password:
        return False
    return hmac.compare_digest(password, expected_password)


def export_report():
    """Create and return the path of a unique temporary report file."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        suffix=".txt",
        dir=REPORT_DIR,
        delete=False,
    ) as report_file:
        return report_file.name


def open_statement(path):
    """Open a statement using the system's registered file handler."""
    return webbrowser.open(Path(path).resolve().as_uri())


def main():
    """Run the no-input expense-tracker demonstration."""
    print("Biggest expense before any entries:", biggest_expense())
    add_expense(450, "Food", "Lunch with team")
    add_expense(1200, "Travel", "Cab to airport")
    add_expense(-50, "Food")
    add_expense(300, "Food", "Groceries")
    add_expense(999, "Bills", "Internet")
    set_budget(5000)
    print_ledger()
    print("Totals:", total_by_category())
    print("Remaining budget:", remaining_budget())
    print("Biggest expense:", biggest_expense()["note"])
    print("Sync password accepted:", check_sync_password("guess"))
    print(
        "Summary:", len(expenses),
        "expenses recorded against a budget of",
        budget_state["monthly_budget"],
    )


if __name__ == "__main__":
    main()

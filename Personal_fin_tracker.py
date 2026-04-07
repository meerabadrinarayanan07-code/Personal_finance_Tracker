import mysql.connector
from datetime import datetime

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1212@',
    'database': 'finance_tracker'
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ------------------- Expense Functions -------------------

def add_expense(amount, category, description, date, payment_mode):
    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO expenses (amount, category, description, date, payment_mode)
               VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(query, (amount, category, description, date, payment_mode))
    conn.commit()
    conn.close()
    print("Expense added successfully!")

def view_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT expense_id, amount, category, description, date, payment_mode FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    print("\n--- Expenses ---")
    for row in rows:
        print(row)

# ------------------- Budget Functions -------------------

def set_budget(category, monthly_limit, current_month):
    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO budgets (category, monthly_limit, current_month)
               VALUES (%s, %s, %s)"""
    cursor.execute(query, (category, monthly_limit, current_month))
    conn.commit()
    conn.close()
    print("Budget set successfully!")

def monthly_summary(month_YYYYMM):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT category, SUM(amount)
    FROM expenses
    WHERE DATE_FORMAT(date, '%Y-%m') = %s
    GROUP BY category;
    """
    cursor.execute(query, (month_YYYYMM,))
    rows = cursor.fetchall()
    conn.close()
    print("\n--- Monthly Summary ---")
    for cat, total in rows:
        print(f"{cat}: {total:.2f}")

# ------------------- Menu -------------------

def menu():
    while True:
        print("\n=== Personal Finance Tracker ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Set Budget")
        print("4. Monthly Summary")
        print("0. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            description = input("Enter description: ")
            date = input("Enter date (YYYY-MM-DD): ")
            payment_mode = input("Enter payment mode: ")
            add_expense(amount, category, description, date, payment_mode)

        elif choice == 2:
            view_expenses()

        elif choice == 3:
            category = input("Enter category: ")
            monthly_limit = float(input("Enter monthly limit: "))
            current_month = datetime.now().strftime('%Y-%m')
            set_budget(category, monthly_limit, current_month)

        elif choice == 4:
            month = datetime.now().strftime('%Y-%m')
            monthly_summary(month)

        elif choice == 0:
            print("Exiting...")
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()

import json
import matplotlib.pyplot as plt

income = 0
expenses = []
transactions = []
savings = 0

def get_user_input(prompt):
    while True:
        try:
            return input(prompt)
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return ""

def validate_amount(amount):
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
        return amount
    except ValueError:
        print("Invalid amount. Please enter a positive number.")
        return None

def validate_category(category):
    if not category:
        print("Invalid category. Please enter a valid category.")
        return None
    return category

def read_transactions_from_file():
    global transactions
    try:
        with open("transactions.json", "r") as file:
            transactions = json.load(file)
    except FileNotFoundError:
        transactions = []

def write_transactions_to_file():
    with open("transactions.json", "w") as file:
        json.dump(transactions, file, indent=4)

def add_income():
    global income
    amount = None
    while amount is None:
        amount = validate_amount(get_user_input("Enter the amount of income: $"))
    income += amount
    transactions.append({"description": "Income", "amount": amount, "category": "Income"})

def add_expense():
    global expenses
    description = None
    while description is None:
        description = validate_category(get_user_input("Enter the description of the expense: "))
    amount = None
    while amount is None:
        amount = validate_amount(get_user_input("Enter the amount of the expense: $"))
    category = None
    while category is None:
        category = validate_category(get_user_input("Enter the category of the expense: "))
    expenses.append({"description": description, "amount": amount, "category": category})
    transactions.append({"description": description, "amount": -amount, "category": category})

def calculate_savings():
    global savings
    savings = income - sum(expense["amount"] for expense in expenses)

def categorize_expenses():
    categories = {}
    for expense in expenses:
        category = expense["category"]
        if category not in categories:
            categories[category] = 0
        categories[category] += expense["amount"]
    return categories

def generate_report():
    categories = categorize_expenses()
    print("\nExpense Report:")
    for category, amount in categories.items():
        print(f"  {category}: ${amount:.2f}")
    print(f"\nTotal Expenses: ${sum(expense['amount'] for expense in expenses):.2f}")
    print(f"Savings: ${savings:.2f}")

def visualize_expenses():
    categories = categorize_expenses()
    labels = list(categories.keys())
    amounts = list(categories.values())
    plt.pie(amounts, labels=labels, autopct="%1.1f%%")
    plt.title("Expense Distribution")
    plt.show()

read_transactions_from_file()

while True:
    print("\nMain Menu:")
    print("  1. Add Income")
    print("  2. Add Expense")
    print("  3. Generate Report")
    print("  4. Visualize Expenses")
    print("  5. Exit")
    choice = get_user_input("Enter your choice: ")
    
    if choice == "1":
        add_income()
    elif choice == "2":
        add_expense()
    elif choice == "3":
        calculate_savings()
        generate_report()
    elif choice == "4":
        visualize_expenses()
    elif choice == "5":
        break
    else:
        print("Invalid choice. Please try again.")

write_transactions_to_file()
print("\nThank you for using the Personal Finance Tracker!")
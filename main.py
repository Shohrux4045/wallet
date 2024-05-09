import sqlite3
class Transaction:
    def __init__(self, amount, category, date):
        self.amount = amount
        self.category = category
        self.date = date

def input_transaction():
    amount = float(input("Enter amount: "))
    category = input("Enter category: ")
    date = input("Enter date (YYYY-MM-DD): ")
    return Transaction(amount, category, date)
class Wallet:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def view_transactions(self):
        for transaction in self.transactions:
            print(f"Amount: {transaction.amount}, Category: {transaction.category}, Date: {transaction.date}")

    def calculate_balance(self):
        total_income = sum(transaction.amount for transaction in self.transactions if transaction.amount > 0)
        total_expense = sum(transaction.amount for transaction in self.transactions if transaction.amount < 0)
        balance = total_income + total_expense
        print(f"Total Income: {total_income}, Total Expense: {total_expense}, Balance: {balance}")

    def filter_transactions_by_category(self, category):
        filtered_transactions = [transaction for transaction in self.transactions if transaction.category == category]
        for transaction in filtered_transactions:
            print(f"Amount: {transaction.amount}, Date: {transaction.date}")



def save_wallet(wallet):
    conn = sqlite3.connect('wallet.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS transactions (amount REAL, category TEXT, date TEXT)")
    c.execute("DELETE FROM transactions")
    for transaction in wallet.transactions:
        c.execute("INSERT INTO transactions VALUES (?, ?, ?)", (transaction.amount, transaction.category, transaction.date))
    conn.commit()
    conn.close()

def load_wallet():
    conn = sqlite3.connect('wallet.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS transactions (amount REAL, category TEXT, date TEXT)")
    c.execute("SELECT * FROM transactions")
    rows = c.fetchall()
    conn.close()
    transactions = []
    for row in rows:
        transactions.append(Transaction(row[0], row[1], row[2]))
    return transactions


def main():
    wallet = Wallet()
    while True:
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Calculate Balance")
        print("4. Filter Transactions by Category")
        print("5. Save Wallet")
        print("6. Load Wallet")
        print("7. Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            transaction = input_transaction()
            wallet.add_transaction(transaction)
        elif choice == "2":
            wallet.view_transactions()
        elif choice == "3":
            wallet.calculate_balance()
        elif choice == "4":
            category = input("Enter category to filter: ")
            wallet.filter_transactions_by_category(category)
        elif choice == "5":
            save_wallet(wallet)
            print("Wallet saved successfully.")
        elif choice == "6":
            wallet.transactions = load_wallet()
            print("Wallet loaded successfully.")
        elif choice == "7":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()


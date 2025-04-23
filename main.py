import sqlite3
from tkinter import *
from tkinter import ttk
from initialize_db import get_accounts_by_name, log_transaction, transfer, initialize_database, view_balance, deposit, withdraw, create_account

def main():
    initialize_database()
    print("Welcome to the Banking App!")
    while True:
        print("\nMenu:")
        print("1. View Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Create Account")
        print("5. Get All Accounts Under Your Name")
        print("6. View Transactions Log") #weird
        print("7. Transfer Between Accounts") #weird
        print("8. Exit")
        choice = input("Choose an option: ")

        if choice == "1": #view balance
            acc_id = int(input("Enter account ID: "))
            balance = view_balance(acc_id)
            if balance is not None:
                print(f"Your balance is: ${balance}")
            else:
                print("Account not found.")
        elif choice == "2": #deposit
            acc_id = int(input("Enter account ID: "))
            amt = float(input("Enter amount to deposit: "))
            deposit(acc_id, amt)
            print("Deposit successful.")
        elif choice == "3": #withdraw
            acc_id = int(input("Enter account ID: "))
            amt = float(input("Enter amount to withdraw: "))
            if withdraw(acc_id, amt):
                print("Withdrawal successful.")
            else:
                print("Insufficient funds or invalid account.")
        elif choice == "4": #create acct
            fName = input("First name: ")
            lName = input("Last name: ")
            acc_type = input("Account type (checkings/savings): ")
            pin = input("PIN: ")
            balance = float(input("Initial deposit: "))
            acc_id = create_account(fName, lName, acc_type, pin, balance)
            print(f"Account created successfully! Your account ID is: {acc_id}")
        elif choice == "5":  # Get All Accounts Under Your Name
            fName = input("Enter your first name: ")
            lName = input("Enter your last name: ")
            accounts = get_accounts_by_name(fName, lName)
            if accounts:
                print("Accounts found:")
                for acc in accounts:
                    print(f"Account ID: {acc[0]}, Type: {acc[1]}, Balance: ${acc[2]:.2f}") # id, type, balance
            else:
                print("No accounts found under this name.")
        elif choice == "6":  # View Transactions Log
            acc_id = int(input("Enter account ID: "))
            with sqlite3.connect('bank.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT action, amount, timestamp FROM transactions WHERE account_id = ?", (acc_id,)) # retrieves transaction for specific account from 'transactions' table
                transactions = cursor.fetchall()
                if transactions:
                    print("\nTransaction History:")
                    for transaction in transactions:
                        print(f"{transaction[2]} | {transaction[0]} | ${transaction[1]:.2f}")
                else:
                    print("No transactions found for this account.")
        elif choice == "7":  # Transfer Between Accounts
            from_acc_id = int(input("Enter sender account ID: "))
            to_acc_id = int(input("Enter recipient account ID: "))
            amt = float(input("Enter amount to transfer: "))
            if transfer(from_acc_id, to_acc_id, amt):
                print("Transfer success!")
            else:
                print("Transfer failed. Check balance or account details.")
        elif choice == "8":
            print("Thank you for stopping by, see you soon!")
            break
        else:
            print("Choose a number listed.")

if __name__ == "__main__":
    main()

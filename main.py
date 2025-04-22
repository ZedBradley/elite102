import sqlite3
from tkinter import *
from tkinter import ttk






def main():
    connection = sqlite3.connect('bank.db')
    cursor = connection.cursor()

    # Get all rows from the students table
    print("Fetching all rows from the users table...")
    results = cursor.execute('''
        SELECT * FROM users
    ''')
    print("Results:")
    for row in results:
        print(row)

    table_accounts = cursor.execute('''
        SELECT * FROM accounts        
    ''')
    print("Results:")
    for acc in table_accounts:
        print(acc)

    # Get all students with a GPA greater than 3.5
    print("Fetching users with last name Marley...")
    results = cursor.execute('''
        SELECT * FROM users WHERE lName = 'Marley'
    ''')
    print("Results:")
    for row in results:
        print(row)
    connection.close()

if __name__ == "__main__":
    main()

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

    # Get all students with a GPA greater than 3.5
    print("Fetching students with last name Marley...")
    results = cursor.execute('''
        SELECT * FROM users WHERE lName = 'Marley'
    ''')
    print("Results:")
    for row in results:
        print(row)
    root = Tk()
    root.title("Simple Tkinter App")

    label = ttk.Label(root, text="Hello, Tkinter!")
    label.pack(pady=20)

    def button_click():
        label.config(text="Button Clicked!")

    button = ttk.Button(root, text="Click Me", command=button_click)
    button.pack(pady=10)

    root.mainloop()

    connection.close()


if __name__ == "__main__":
    main()

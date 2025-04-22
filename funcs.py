import sqlite3
connection = sqlite3.connect('bank.db')
cursor = connection.cursor()


def view_balance(entered_pin):
    results = cursor.execute('''
        SELECT * FROM accounts WHERE pin = entered_pin
    ''')
    print('balance:')
    for row in results:
        print(row)

print('all good')
connection.close()

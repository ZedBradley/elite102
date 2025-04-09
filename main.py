import sqlite3


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

    connection.close()


if __name__ == "__main__":
    main()

import sqlite3

DB_NAME = 'bank.db'


def initialize_database():
    connection = sqlite3.connect(DB_NAME)
    print("Connected to the database.")
    cursor = connection.cursor()
    print("Cursor created.")
    # Create a sample table
    print("Creating table if it does not exist...")
    cursor.execute('''
        CREATE TABLE users
            (id integer primary key, 
            fName text,
            lName text, 
            email text,
            phone_number text)
    ''')
    # cursor.execute('''
    #     CREATE TABLE accounts
    #         (id integer primary key, 
    #         fName text,
    #         lName text, 
    #         email text,
    #         phone number text)
    # ''')

    print("Table created.")

    # Insert sample data
    print("Inserting sample data...")
    cursor.execute('''
        INSERT INTO users (fName, lName, email, phone_number) VALUES
        ('Alice', 'Jones', 'Alice@test.com', '555-555-5555'),
        ('Bob', 'Marley','Bob@test.com', '554-445-4444'),
        ('Charlie', 'Barley','Charlie@test.com', '553-335-3333')
    ''')
    print("Sample data inserted.")
    # Commit the changes and close the connection
    print("Committing changes and closing the connection...")
    connection.commit()
    connection.close()


initialize_database()

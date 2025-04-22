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
            phone_number text,
            SSN_4_dig)
    ''')
    print("Table created.")

    cursor.execute('''
        CREATE TABLE accounts
            (id integer primary key, 
            fName text,
            lName text,
            type, 
            pin,
            balance)
    ''')

    print("Table created.")

    # Insert sample data
    print("Inserting sample data...")
    cursor.execute('''
        INSERT INTO users (fName, lName, email, phone_number, SSN_4_dig) VALUES
        ('Alice', 'Jones', 'Alice@test.com', '555-555-5555', '0897'),
        ('Bob', 'Marley','Bob@test.com', '554-445-4444', '8649'),
        ('Charlie', 'Barley','Charlie@test.com', '553-335-3333', '8832')
    ''')

    print("Inserting sample data2...")
    cursor.execute('''
        INSERT INTO accounts (fName, lName, type, pin, balance) VALUES
        ('Alice', 'Jones', 'checkings', '1234', '10,724'),
        ('Bob', 'Marley',  'savings', '0987', '3,000'),
        ('Charlie', 'Barley', 'savings','4535', '12,090')
    ''')

    
    print("Sample data inserted.")
    # Commit the changes and close the connection
    print("Committing changes and closing the connection...")
    connection.commit()
    connection.close()


initialize_database()

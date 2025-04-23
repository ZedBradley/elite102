import sqlite3

DB_NAME = 'bank.db'

def initialize_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            fName TEXT,
            lName TEXT, 
            email TEXT,
            phone_number TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER,
            type TEXT, 
            pin TEXT,
            balance REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''') #REAL is SQL version of float

    connection.commit()
    connection.close()

def view_balance(account_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,)) # '?' placeholder for variables, safer then putting names in
        result = cursor.fetchone()
        return result[0] if result else None

def deposit(account_id, amount):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
        conn.commit()
        log_transaction(account_id, 'deposit', amount)  # Log the transaction

def withdraw(account_id, amount):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
        balance = cursor.fetchone()
        if balance and balance[0] >= amount:
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))
            conn.commit()
            log_transaction(account_id, 'withdraw', amount)  # Log the transaction
            return True
        return False


def create_account(fName, lName, acc_type, pin, balance):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # Insert into users table
        cursor.execute(
            """
            INSERT INTO users (fName, lName, email, phone_number)
            VALUES (?, ?, '', '')
            """,
            (fName, lName)
        )
        user_id = cursor.lastrowid  # Get the ID of the newly inserted user
        
        # Insert into accounts table using the user_id
        cursor.execute(
            """
            INSERT INTO accounts (user_id, type, pin, balance)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, acc_type, pin, balance)
        )
        account_id = cursor.lastrowid  # Get the account ID
        conn.commit()

        
        return account_id

def transfer(from_acc_id, to_acc_id, amount):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Check sender balance
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (from_acc_id,)) # search for account w/ id
        result = cursor.fetchone()
        if not result or result[0] < amount:
            return False
        # transfer
        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_acc_id)) # ? act as placeholders that get placed in automatically
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_acc_id))
        log_transaction(from_acc_id, 'transfer_out', amount) #log the out
        log_transaction(to_acc_id, 'transfer_in', amount) #log the in
        conn.commit()
        return True

def log_transaction(account_id, action, amount):
    """ Logs a transaction while ensuring the database doesn't lock. """
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.execute("PRAGMA journal_mode=WAL")  # prevent the damn locks
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                action TEXT,
                amount REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            INSERT INTO transactions (account_id, action, amount)
            VALUES (?, ?, ?)
        ''', (account_id, action, amount))

        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}") # helping stop the database locks
    finally:
        conn.close()  


def get_accounts_by_name(fName, lName):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT accounts.id, type, balance
            FROM accounts
            JOIN users ON accounts.user_id = users.id 
            WHERE users.fName = ? AND users.lName = ?
        ''', (fName, lName))
        #above joins accounts and users then finds entries with fname and lname
        return cursor.fetchall() # returns results from last query


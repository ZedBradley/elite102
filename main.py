from flask import Flask, redirect, url_for, render_template, request, flash
from initialize_db import (
    get_accounts_by_name, log_transaction, transfer,
    initialize_database, view_balance, deposit,
    withdraw, create_account
)

app = Flask(__name__)
app.secret_key = "Zedekiah Bradley Secret Key"  # Needed for flash messages

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Account registration form
@app.route('/register')
def register():
    return render_template('register.html')

# Registration action
@app.route('/register_action', methods=['POST']) #POST for form submission
def register_action():
    fName = request.form['fName']
    lName = request.form['lName']
    acc_type = request.form['acc_type']
    pin = request.form['pin']
    balance = float(request.form['balance'])
    account_id = create_account(fName, lName, acc_type, pin, balance)
    flash(f'Account created with ID: {account_id}')
    return redirect(url_for('home'))

# View accounts by name
@app.route('/accounts', methods=['GET', 'POST']) # get for opening page, post for form submission
def accounts():
    accounts = []
    if request.method == 'POST':
        fName = request.form['fName']
        lName = request.form['lName']
        accounts = get_accounts_by_name(fName, lName)
    return render_template('accounts.html', accounts=accounts)

# View balance
@app.route('/balance/<int:account_id>')
def balance(account_id):
    bal = view_balance(account_id)
    return render_template('balance.html', balance=bal, account_id=account_id)

# Deposit
@app.route('/deposit', methods=['GET', 'POST'])
def deposit_page():
    if request.method == 'POST':
        acc_id = int(request.form['account_id'])
        amount = float(request.form['amount'])
        deposit(acc_id, amount)
        flash('Deposit successful.')
        return redirect(url_for('home'))
    return render_template('deposit.html')


# Withdraw
@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw_page():
    if request.method == 'POST':
        acc_id = int(request.form['acc_id'])
        amount = float(request.form['amount'])
        if withdraw(acc_id, amount):
            flash('Withdrawal successful!')
        else:
            flash('Insufficient funds or account does not exist.')
        return redirect(url_for('home'))
    return render_template('withdraw.html')

# Transfer
@app.route('/transfer', methods=['GET', 'POST'])
def transfer_page():
    if request.method == 'POST':
        from_id = int(request.form['from_account'])
        to_id = int(request.form['to_account'])
        amount = float(request.form['amount'])
        if transfer(from_id, to_id, amount):
            flash('Transfer successful.')
        else:
            flash('Transfer failed (insufficient funds or invalid account).')
        return redirect(url_for('home'))
    return render_template('transfer.html')

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, host='0.0.0.0', port=8000)

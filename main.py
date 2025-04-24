from flask import Flask, redirect, url_for, flash, render_template, session, request
from initialize_db import view_balance, create_account


app = Flask(__name__)

# @app.context_processor
# def inject_functions():
#     functions = {view_balance:view_balance}
#     return functions
app.jinja_env.globals.update(view_balance=view_balance)
app.jinja_env.globals.update(create_account=create_account)




@app.route('/')
def home():
    return render_template('home.html')

@app.route('/accounts/<int:id>')
def account(id):
    return render_template('accounts.html', id=id)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register_action', methods=['POST'])
def register_action():
    fName = request.form['fName']
    lName = request.form['lName']
    acc_type = request.form['acc_type']
    pin = request.form['pin']
    balance = request.form['balance']
    create_account(fName, lName, acc_type, pin, balance)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
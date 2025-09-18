from flask import Flask, render_template, request, url_for, flash, redirect, jsonify 
from sqlalchemy import func
from datetime import datetime
from decimal import Decimal, InvalidOperation
from models import db, AccountType, Account, Transaction
from dotenv import load_dotenv
import os
from helper_funcs import setup_test_db

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'SECRET-DEV-KEY'
app.config['APP_ENV'] = os.environ.get('APP_ENV')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def index():
    accounts = Account.query.filter(Account.is_active).all()
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()

    return render_template('dashboard.html',
                           accounts=accounts,
                           transactions=transactions)

@app.route('/accounts', methods=['GET', 'POST'])
def accounts():
    if request.method == 'POST':
        account_name = request.form['account-name']
        account_type = request.form['account-type']

        try:
            account_type = AccountType[account_type]
        except KeyError:
            flash('Incorrect Account Type', 'error')
            return redirect(url_for('add_account'))

        existing_account = Account.query.filter(
            func.lower(Account.name) == func.lower(account_name),
            Account.is_active
        ).first()
        if existing_account:
            flash('Account with this name already exists!', 'error')
            return redirect(url_for('add_account'))

        new_account = Account(account_name=account_name, account_type=account_type)

        try:
            db.session.add(new_account)
            db.session.commit()
            flash(f'Account {account_name} added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding account: {str(e)}', 'error')
            return redirect(url_for('add_account'))
    else:
        accounts = db.session.execute(
            db.select(Account).where(
                Account.is_active
            )
        ).scalars().all()

        return render_template('accounts.html', accounts=accounts)


@app.route('/accounts/new', methods=['GET'])
def add_account():
    return render_template('add_account.html')


@app.route('/accounts/<int:account_id>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def update_or_delete_account(account_id):
    """Update or Delete Account"""
    if request.method == 'POST' and '_method' in request.form:
        request.method = request.form['_method'].upper()

    if request.method == 'DELETE':
        account = Account.query.get_or_404(account_id)
        account.is_active = False

        try:
            db.session.commit()
            return jsonify({
                'message': f'Account {account.name} successfully marked inactive!',
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': f'Error marking account inactive: {str(e)}'
            }), 500
    elif request.method == 'PATCH':
        account_new_name = request.form['account-name']
        account = Account.query.get_or_404(account_id)

        if account.name == account_new_name:
            flash(f'Account {account.name} has not been modified!')
            return redirect(url_for('index'))

        existing_account = Account.query.filter(
            func.lower(Account.name) == func.lower(account_new_name)
        ).first()
        if existing_account:
            flash(f"Account with the name '{account_new_name}' already exists!", 'error')
            return render_template('update_account.html', account=account)

        account.name = account_new_name

        try:
            db.session.commit()
            flash(f'Account Name {account.name} updated successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': f'Error updating account: {str(e)}'
            }), 500
    else:
        account = Account.query.get_or_404(account_id)
        return render_template('update_account.html', account=account)


@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if request.method == 'POST':
        description = request.form['transaction-description']
        date = datetime.strptime(request.form['transaction-date'], '%Y-%m-%d')
        amount = request.form['transaction-amount']
        debit_account_id = request.form['transaction-debit-account']
        credit_account_id = request.form['transaction-credit-account']

        try:
            amount = Decimal(amount)
        except InvalidOperation:
            flash('Amount must be a $ Value', 'error')
            return redirect(url_for('add_transaction'))

        if debit_account_id == credit_account_id:
            flash('Debit and Credit Accounts cannot be the same', 'error')
            return redirect(url_for('add_transaction'))

        new_transaction = Transaction(
            description=description,
            date=date,
            amount=amount,
            debit_account_id=debit_account_id,
            credit_account_id=credit_account_id
        )

        try:
            db.session.add(new_transaction)
            db.session.commit()
            flash('Transaction created successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating transaction: {str(e)}', 'error')
            return redirect(url_for('add_transaction'))
    else:
        transactions = Transaction.query.order_by(Transaction.date.desc()).all()
        return render_template('transactions.html', transactions=transactions)


@app.route('/transactions/new', methods=['GET', 'POST'])
def add_transaction():
    accounts = Account.query.filter(
        Account.is_active
    ).all()
    return render_template('add_transaction.html', accounts=accounts)


@app.route('/transactions/<int:transaction_id>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def update_or_delete_transaction(transaction_id):
    """Update or Delete Transaction"""
    if request.method == 'POST' and '_method' in request.form:
        request.method = request.form['_method'].upper()

    if request.method == 'DELETE':
        transaction = Transaction.query.get_or_404(transaction_id)
        transaction.is_active = False

        try:
            db.session.commit()
            return jsonify({
                'message': f'Transaction \'{transaction.id}\' marked as deleted!',
                'debitAccount': {
                    'id': transaction.debit_account.id,
                    'balance': transaction.debit_account.get_balance(),
                },
                'creditAccount': {
                    'id': transaction.credit_account.id,
                    'balance': transaction.credit_account.get_balance(),
                },
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': f'Error deleting transaction: {str(e)}'
            }), 500
    elif request.method == 'PATCH':
        accounts = Account.query.filter(Account.is_active).all()
        transaction = Transaction.query.get_or_404(transaction_id)

        description = request.form['transaction-description']
        date = datetime.strptime(request.form['transaction-date'], '%Y-%m-%d')
        amount = request.form['transaction-amount']
        debit_account_id = request.form['transaction-debit-account']
        credit_account_id = request.form['transaction-credit-account']

        try:
            amount = Decimal(amount)
        except InvalidOperation:
            flash('Amount must be a $ Value', 'error')
            return render_template('update_transaction.html', transaction=transaction, accounts=accounts)

        if debit_account_id == credit_account_id:
            flash('Debit and Credit Accounts cannot be the same', 'error')
            return render_template('update_transaction.html', transaction=transaction, accounts=accounts)
        
        transaction.description = description
        transaction.date = date
        transaction.amount = amount
        transaction.debit_account_id = debit_account_id
        transaction.credit_account_id = credit_account_id

        try:
            db.session.commit()
            flash(f'Transaction updated successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating Transaction {transaction.id}', 'error')
            return jsonify({
                'error': f'Error updating account: {str(e)}'
            }), 500
    else:
        accounts = Account.query.filter(Account.is_active).all()
        transaction = Transaction.query.get_or_404(transaction_id)
        return render_template('update_transaction.html', transaction=transaction, accounts=accounts)


if __name__ == '__main__':
    with app.app_context():
        if app.config['APP_ENV'] == 'DEV':
            setup_test_db(app)
        else:
            db.create_all()

        app.run(host='0.0.0.0', port=5001, debug=True)

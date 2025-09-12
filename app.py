from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from sqlalchemy import func
from datetime import datetime
from decimal import Decimal
from models import db, AccountType, Account, Transaction
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pft.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'SECRET-DEV-KEY'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def index():
    accounts = Account.query.filter(
        Account.is_active
    ).all()
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()

    return render_template('dashboard.html',
                           accounts=accounts,
                           transactions=transactions)


@app.route('/add_account', methods=['GET', 'POST'])
def add_account():
    """Add a new account"""
    if request.method == 'POST':
        account_name = request.form['account-name']
        account_type = request.form['account-type']

        try:
            account_type = AccountType[account_type]
        except KeyError:
            flash('Incorrect Account Type', 'error')

        existing_account = Account.query.filter(
            func.lower(Account.name) == func.lower(account_name)
        ).first()
        if existing_account:
            flash('Account with this name already exists!', 'error')
            return redirect(url_for('add_account'))

        new_account = Account(name=account_name, account_type=account_type)

        try:
            db.session.add(new_account)
            db.session.commit()
            flash(f'Account {account_name} added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding account: {str(e)}', 'error')

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


@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    """Add a new transaction"""
    if request.method == 'POST':
        description = request.form['description']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        amount = request.form['amount']
        debit_account_id = request.form['debit-account']
        credit_account_id = request.form['credit-account']

        if not amount.isdigit():
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

    accounts = Account.query.filter(
        Account.is_active
    ).all()
    return render_template('add_transaction.html', accounts=accounts)


@app.route('/transactions/<int:transaction_id>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def update_or_delete_transaction(transaction_id):
    """Update or Delete Account"""
    if request.method == 'POST' and '_method' in request.form:
        request.method = request.form['_method'].upper()

    if request.method == 'DELETE':
        transaction = Transaction.query.get_or_404(transaction_id)
        transaction.is_active = False

        try:
            db.session.commit()
            return jsonify({
                'message': f'Transaction {transaction.id} marked as deleted!',
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
                'error': f'Error marking account inactive: {str(e)}'
            }), 500
    elif request.method == 'PATCH':
        return jsonify({'message': 'Not Implemented'}), 500
    else:
        return jsonify({'message': 'Not Implemented'}), 500


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        checking = Account(name="Checking",
                           account_type=AccountType.ASSET)
        salary = Account(name="Salary",
                         account_type=AccountType.INCOME)
        groceries = Account(name="Groceries",
                            account_type=AccountType.EXPENSE)
        credit = Account(name="Credit Card",
                         account_type=AccountType.LIABILITY)
        equity = Account(name="Equity",
                         account_type=AccountType.EQUITY)
        accounts = [checking, salary, groceries, credit, equity]
        db.session.add_all(accounts)
        db.session.commit()

        opening_balance_transaction = Transaction(description='Opening Balance',
                                                  date=datetime.now(),
                                                  amount=Decimal('1750.50'),
                                                  debit_account_id=checking.id,
                                                  credit_account_id=equity.id)
        groceries_transaction = Transaction(description='Paid for Groceries',
                                            date=datetime.now(),
                                            amount=Decimal('153.27'),
                                            debit_account_id=groceries.id,
                                            credit_account_id=checking.id)
        income_transaction = Transaction(description='Biweekly Salary Payment',
                                         date=datetime.now(),
                                         amount=Decimal('3725.25'),
                                         debit_account_id=checking.id,
                                         credit_account_id=salary.id)
        credit_transaction = Transaction(description='Paid for Groceries',
                                         date=datetime.now(),
                                         amount=Decimal('87.56'),
                                         debit_account_id=groceries.id,
                                         credit_account_id=credit.id)
        transactions = [opening_balance_transaction, groceries_transaction,
                        income_transaction, credit_transaction]
        db.session.add_all(transactions)
        db.session.commit()

    app.run(debug=True)

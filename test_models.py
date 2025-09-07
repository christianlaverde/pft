#!/usr/bin/python3

from flask import Flask
from models import db, Account, AccountType, Transaction
from datetime import datetime
from decimal import Decimal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def test_models():
    with app.app_context():
        print('Creating DB tables...\n')
        db.drop_all()
        db.create_all()

        print("Creating Accounts...")
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

        db.session.add_all([checking, salary, groceries, credit, equity])
        db.session.commit()

        print(f'Created: {checking}')
        print(f'\tNormalBalance: {checking.normal_balance}')
        print(f'Created: {salary}')
        print(f'\tNormalBalance: {salary.normal_balance}')
        print(f'Created: {groceries}')
        print(f'\tNormalBalance: {groceries.normal_balance}')
        print(f'Created: {credit}')
        print(f'\tNormalBalance: {credit.normal_balance}')
        print(f'Created: {equity}')
        print(f'\tNormalBalance: {equity.normal_balance}')

        print('\nCreating Transactions...')
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

        db.session.add_all([opening_balance_transaction, groceries_transaction, income_transaction, credit_transaction])
        db.session.commit()

        print(f'Created: {opening_balance_transaction}')
        print(f'Created: {groceries_transaction}')
        print(f'Created: {income_transaction}')
        print(f'Created: {credit_transaction}')



test_models()

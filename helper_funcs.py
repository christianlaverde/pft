#!/usr/bin/python3

from models import db, Account, AccountType, Transaction
from datetime import datetime
from decimal import Decimal


def setup_test_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

        checking = Account(account_name="Checking",
                           account_type=AccountType.ASSET)
        salary = Account(account_name="Salary",
                         account_type=AccountType.INCOME)
        groceries = Account(account_name="Groceries",
                            account_type=AccountType.EXPENSE)
        credit = Account(account_name="Credit Card",
                         account_type=AccountType.LIABILITY)
        equity = Account(account_name="Equity",
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

        db.session.add_all([opening_balance_transaction, groceries_transaction, income_transaction, credit_transaction])
        db.session.commit()

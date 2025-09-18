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
        savings = Account(account_name='Savings',
                          account_type=AccountType.ASSET)
        cash = Account(account_name='Cash',
                       account_type=AccountType.ASSET)
        salary = Account(account_name="Salary",
                         account_type=AccountType.INCOME)
        groceries = Account(account_name="Groceries",
                            account_type=AccountType.EXPENSE)
        rent = Account(account_name="Rent",
                       account_type=AccountType.EXPENSE)
        credit = Account(account_name="Credit Card",
                         account_type=AccountType.LIABILITY)
        equity = Account(account_name="Equity",
                         account_type=AccountType.EQUITY)
        accounts = [checking, savings, cash, salary, groceries, rent, credit, equity]
        db.session.add_all(accounts)
        db.session.commit()

        opening_balance_checking = Transaction(description='Opening Balance for Checking',
                                               date=datetime.now(),
                                               amount=Decimal('1750.50'),
                                               debit_account_id=checking.id,
                                               credit_account_id=equity.id)
        opening_balance_savings = Transaction(description='Opening Balance for Savings',
                                              date=datetime.now(),
                                              amount=Decimal('1500.00'),
                                              debit_account_id=savings.id,
                                              credit_account_id=equity.id)
        opening_balance_cash = Transaction(description='Opening Balance for Cash',
                                           date=datetime.now(),
                                           amount=Decimal('75.00'),
                                           debit_account_id=cash.id,
                                           credit_account_id=equity.id)
        groceries_tr = Transaction(description='Paid for Groceries',
                                   date=datetime.now(),
                                   amount=Decimal('153.27'),
                                   debit_account_id=groceries.id,
                                   credit_account_id=checking.id)
        rent_tr = Transaction(description='Paid Rent',
                              date=datetime.now(),
                              amount=Decimal('900.00'),
                              debit_account_id=rent.id,
                              credit_account_id=checking.id)
        transactions = [opening_balance_checking]
        income_tr = Transaction(description='Biweekly Salary Payment',
                                date=datetime.now(),
                                amount=Decimal('3725.25'),
                                debit_account_id=checking.id,
                                credit_account_id=salary.id)
        credit_tr = Transaction(description='Paid for Groceries',
                                date=datetime.now(),
                                amount=Decimal('87.56'),
                                debit_account_id=groceries.id,
                                credit_account_id=credit.id)
        transactions = [
            opening_balance_checking, opening_balance_cash, opening_balance_savings,
            groceries_tr, rent_tr,  income_tr, credit_tr
        ]

        db.session.add_all(transactions)
        db.session.commit()

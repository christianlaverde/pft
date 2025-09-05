#!/usr/bin/python3

from flask import Flask
from models import db, Account, AccountType

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def test_models():
    with app.app_context():
        print('Creating DB tables...')
        db.drop_all()
        db.create_all()

        print("Creating Accounts...")
        checking = Account(name="Checking",
                           account_type=AccountType.ASSET)
        groceries = Account(name="Groceries",
                            account_type=AccountType.EXPENSE)
        equity = Account(name="Equity",
                         account_type=AccountType.EQUITY)

        db.session.add_all([checking, groceries, equity])
        db.session.commit()

        print(f'Created: {checking}')
        print(f'\tNormalBalance: {checking.normal_balance}')
        print(f'Created: {groceries}')
        print(f'\tNormalBalance: {groceries.normal_balance}')
        print(f'Created: {equity}')
        print(f'\tNormalBalance: {equity.normal_balance}')


test_models()

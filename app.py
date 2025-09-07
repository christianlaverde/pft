from flask import Flask, render_template
from datetime import datetime
from decimal import Decimal
from models import db, AccountType, Account, Transaction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pft.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def index():
    accounts = Account.query.all()
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()

    return render_template('dashboard.html',
                           accounts=accounts,
                           transactions=transactions)


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

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class AccountType(Enum):
    ASSET = 'ASSET'
    LIABILITY = 'LIABILITY'
    EQUITY = 'EQUITY'
    INCOME = 'INCOME'
    EXPENSE = 'EXPENSE'


class NormalBalance(Enum):
    DEBIT = 'DEBIT'
    CREDIT = 'CREDIT'


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.Enum(AccountType), nullable=False)
    normal_balance = db.Column(db.Enum(NormalBalance), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, name, account_type):
        self.name = name
        self.account_type = account_type
        self.normal_balance = self._get_normal_balance()

    def _get_normal_balance(self):
        """Returns normal balance based on account type"""
        if self.account_type in (AccountType.ASSET, AccountType.EXPENSE):
            return NormalBalance.DEBIT
        else:
            return NormalBalance.CREDIT

    def get_balance(self):
        """Returns running balance"""
        debit_transactions = Transaction.query.filter_by(debit_account_id=self.id).all()
        credit_transactions = Transaction.query.filter_by(credit_account_id=self.id).all()

        total_debits = sum(dt.amount for dt in debit_transactions)
        total_credits = sum(ct.amount for ct in credit_transactions)

        if self.normal_balance == NormalBalance.DEBIT:
            balance = total_debits - total_credits
        else:
            balance = total_credits - total_debits

        return balance

    def __repr__(self):
        return f'<Account {self.name}[{self.id}] ({self.account_type})>'


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    debit_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    credit_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    debit_account = db.relationship('Account', foreign_keys=[debit_account_id])
    credit_account = db.relationship('Account', foreign_keys=[credit_account_id])

    def __init__(self, description, date, amount, debit_account_id, credit_account_id):
        self.description = description
        self.date = date
        self.amount = amount
        self.debit_account_id = debit_account_id
        self.credit_account_id = credit_account_id

    def __repr__(self):
        return f'<Transaction ${self.amount} paid to {self.debit_account_id} by {self.credit_account_id} for {self.description} on {self.date}>'

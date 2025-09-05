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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, account_type):
        self.name = name
        self.account_type = account_type
        self.normal_balance = self._get_normal_balance()

    def _get_normal_balance(self):
        """Sets normal balance based on account type"""
        if self.account_type in (AccountType.ASSET, AccountType.EXPENSE):
            return NormalBalance.DEBIT
        else:
            return NormalBalance.CREDIT

    def __repr__(self):
        return f'<Account {self.name} ({self.account_type})>'

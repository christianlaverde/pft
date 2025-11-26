#!/usr/bin/python3

from app.models import db
from sqlalchemy import text
import os


def setup_test_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

        sql_seed_data_file_path = os.path.join(os.path.dirname(__file__), 'seed_data.sql')
        with open(sql_seed_data_file_path, 'r') as f:
            sql_script = f.read()

        statements = [s.strip() for s in sql_script.split(';') if s.strip()]
        for statement in statements:
            db.session.execute(text(statement))

        db.session.commit()



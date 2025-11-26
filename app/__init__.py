from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

from app.models import db


def create_app():
    app = Flask(__name__,
                static_folder='static',
                template_folder='templates')

    app.config['APP_ENV'] = os.environ.get('APP_ENV')
    if app.config['APP_ENV'] == 'DEV':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEV_DATABASE_URI')
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'SECRET-DEV-KEY'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes import register_routes
    register_routes(app)

    return app

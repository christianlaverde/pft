from app import create_app, db
from app.utils import setup_test_db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        if app.config['APP_ENV'] == 'DEV':
            setup_test_db(app)
        else:
            db.create_all()

        app.run(host='0.0.0.0', port=5001, debug=True)

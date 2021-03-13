from argparse import ArgumentParser

from flask import Flask

from src.app import AppConfig
from src.models import db

"""
Creates the database if it does not already exist and creates all the tables inside if it
Can be run with the --delete command line flag to empty the existing database
"""
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--delete', help="DELETES ALL DATA in the database and starts over", action='store_true')

    drop_all = parser.parse_args().delete

    app = Flask(__name__)
    app.config.from_object(AppConfig())
    db.init_app(app)
    with app.app_context():
        if drop_all:
            db.drop_all()

        db.create_all()

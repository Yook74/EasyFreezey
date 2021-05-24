from os import path

from flask import Flask
from sqlalchemy.exc import IntegrityError

from src.models import db
from src.routes import blueprints
from src.handlers import *


class AppConfig:
    use_sqlite = False
    db_username = 'freezey-flask'
    db_host = 'soup.tplinkdns.com'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def db_password(self):
        with open('db_password.txt') as password_file:
            return password_file.read().strip()

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        if self.use_sqlite:
            db_path = path.abspath('easy-freezey.db')
            return 'sqlite:///' + db_path
        else:
            return f'postgresql://{self.db_username}:{self.db_password}@{self.db_host}:5432/easy_freezey'


def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig())
    db.init_app(app)

    with app.app_context():
        for blueprint in blueprints:
            app.register_blueprint(blueprint)

        app.register_error_handler(KeyError, handle_key_error)
        app.register_error_handler(IntegrityError, handle_integrity_error)

    return app


if __name__ == '__main__':
    create_app().run()

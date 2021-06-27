from os import path

from flask import Flask
from sqlalchemy.exc import IntegrityError, StatementError
from werkzeug.exceptions import NotFound, BadRequest

from server.models import db
from server.routes import blueprints
from server.handlers import *


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
        app.register_error_handler(ValueError, handle_value_error)
        app.register_error_handler(StatementError, handle_value_error)  # StatementError is a subclass of ValueError
        app.register_error_handler(NotFound, handle_not_found)
        app.register_error_handler(BadRequest, handle_bad_request)

    return app


if __name__ == '__main__':
    create_app().run()

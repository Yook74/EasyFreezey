from os import path

from flask import Flask

from src.models import db


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
        import routes
        return app


application = create_app()  # Gunicorn uses this application object

if __name__ == '__main__':
    application.run()

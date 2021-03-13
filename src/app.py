from os import path

from flask import Flask

from src.models import db


class AppConfig:
    use_sqlite = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        if self.use_sqlite:
            db_path = path.abspath('easy-freezey.db')
            return 'sqlite:///' + db_path
        else:
            raise NotImplemented()


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

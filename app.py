from flask import Flask
from extensao import db, migrate
from routes.inicio import web


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(web)

    return app


if __name__ == '__main__':
    create_app()

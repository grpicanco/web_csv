from flask import Flask
from extensao import db, migrate
from routes.inicio import web
from routes.api import api


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(web)
    app.register_blueprint(api)

    return app


if __name__ == '__main__':
    create_app()

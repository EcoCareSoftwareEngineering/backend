from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    from . import models

    from .routes import main

    app.register_blueprint(main)

    @app.errorhandler(404)
    def page_not_found(error):
        return {"Error": "Invalid URL"}

    return app

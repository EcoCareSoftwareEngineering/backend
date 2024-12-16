from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .routes import main

    app.register_blueprint(main)

    @app.errorhandler(404)
    def page_not_found(error):
        return {"Error": "Invalid URL"}

    with app.app_context():
        from .models import IoTDevices

        db.create_all()

    return app

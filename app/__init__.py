import os, json
from flask import Flask
from flask_migrate import Migrate, init, migrate, upgrade
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from alembic import autogenerate
from alembic.migration import MigrationContext

from .config import Config


db = SQLAlchemy()


with open("config/smart_home_config.json") as file:
    local_device_config = json.load(file)


def create_app():
    from . import models
    from .data import add_data_check
    from .routes import register_routes

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    CORS(app)

    with app.app_context():
        if not os.path.exists(os.path.join(os.getcwd(), "migrations")):
            init()
            migrate()
            upgrade()

        conn = db.engine.connect()
        migration_context = MigrationContext.configure(conn)

        if bool(autogenerate.compare_metadata(migration_context, db.metadata)):
            migrate()
            upgrade()

        add_data_check()

    register_routes(app)

    return app

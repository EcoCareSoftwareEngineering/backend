from flask import Flask
from flask_migrate import Migrate, init, migrate, upgrade
from flask_sqlalchemy import SQLAlchemy
from alembic import autogenerate
from alembic.migration import MigrationContext

from .config import Config


db = SQLAlchemy()


def create_app():
    from . import models
    from .data import add_data
    from .routes import register_routes

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        # init()

        conn = db.engine.connect()
        migration_context = MigrationContext.configure(conn)

        if bool(autogenerate.compare_metadata(migration_context, db.metadata)):
            migrate()
            upgrade()

        add_data()

    register_routes(app)

    return app

import os, json
from flask_socketio import SocketIO
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

unconnected_iot_devices = []

""" Uncomment this definition if not using spoof app so can still have unconnected IoT devices """
# unconnected_iot_devices = [
#     {
#         "ipAddress": "192.168.0.9",
#         "name": "Smart Light",
#         "description": "A smart lightbulb",
#         "state": [],
#         "status": "On",
#         "faultStatus": "Ok",
#     },
#     {
#         "ipAddress": "192.168.0.10",
#         "name": "Smart Lock",
#         "description": "A smart lock",
#         "state": [{"fieldName": "engaged", "datatype": "boolean", "value": True}],
#         "status": "On",
#         "faultStatus": "Ok",
#     },
# ]


def create_app():
    from . import models
    from .data import add_data_check
    from .routes import register_routes
    from .websockets.events import register_socketio_handlers

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    CORS(app)
    global socketio
    socketio = SocketIO(app)

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
    register_socketio_handlers(socketio)

    return app, socketio

from flask import Blueprint
from .blueprints.devices import devices_blueprint

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

api_blueprint.register_blueprint(devices_blueprint)

from flask import Blueprint
from .blueprints.automation import automations_blueprint
from .blueprints.devices import devices_blueprint
from .blueprints.energy import energy_blueprint
from .blueprints.goals import goals_blueprint
from .blueprints.misc import misc_blueprint
from .blueprints.reports import reports_blueprint
from .blueprints.tags import tags_blueprint

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

api_blueprint.register_blueprint(automations_blueprint)
api_blueprint.register_blueprint(devices_blueprint)
api_blueprint.register_blueprint(energy_blueprint)
api_blueprint.register_blueprint(goals_blueprint)
api_blueprint.register_blueprint(misc_blueprint)
api_blueprint.register_blueprint(reports_blueprint)
api_blueprint.register_blueprint(tags_blueprint)

from .blueprints.dev import dev_blueprint

development_blueprint = Blueprint("development", __name__, url_prefix="/dev")
development_blueprint.register_blueprint(dev_blueprint)

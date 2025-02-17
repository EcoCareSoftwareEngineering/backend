from functools import wraps
from flask import jsonify, request

from . import local_device_config, tokens


def register_routes(app):

    @app.errorhandler(404)
    def error_handler(error):
        return jsonify({"Error": "Invalid URL"}), 500

    from .api import api_blueprint, development_blueprint

    app.register_blueprint(api_blueprint)
    app.register_blueprint(development_blueprint)


def check_token(function):
    @wraps(function)
    def check_token_helper(*args, **kwargs):
        token = request.headers.get("token")

        if token is None:
            return jsonify({"Error": "Missing authorisation token"}), 500

        if not token in [tokens["local"], *tokens["remote"]]:
            return jsonify({"Error": "Missing authorisation token"}), 500

        if token == tokens["local"] and local_device_config["locked"]:
            return jsonify({"Error": "Touchscreen Locked"}), 500

        return function(*args, **kwargs)

    return check_token_helper

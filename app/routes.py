from flask import jsonify


def register_routes(app):

    @app.errorhandler(404)
    def error_handler(error):
        return jsonify({"Error": "Invalid URL"}), 500

    from .api import api_blueprint, development_blueprint

    app.register_blueprint(api_blueprint)
    app.register_blueprint(development_blueprint)

from flask import Blueprint, jsonify

from ...data import reset_db

dev_blueprint = Blueprint("dev", __name__, url_prefix="")


@dev_blueprint.route("/resetdb/", methods=["POST"])
def reset_db_handler():
    reset_db()
    return jsonify(""), 200

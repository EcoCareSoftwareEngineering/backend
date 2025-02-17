from flask import Blueprint, jsonify, request
from sqlalchemy import select, insert, update, delete

from ...models import *
from ... import db, local_device_config

misc_blueprint = Blueprint("misc", __name__, url_prefix="")


@misc_blueprint.route("/unlock/", methods=["GET", "POST"])
def misc_handler():
    if request.method == "GET":
        return get_misc_handler()
    elif request.method == "POST":
        return post_misc_handler()
    return jsonify({"endpoint": "GET_misc_handler"}), 500


def get_misc_handler():
    return jsonify({"pinEnabled": local_device_config["pinCode"] != ""}), 200


def post_misc_handler():
    json = request.json

    if json is None:
        return jsonify({}), 500

    if json["pinCode"] == local_device_config["pinCode"]:
        local_device_config["locked"] = False

        return jsonify({local_device_config["locked"]}), 200

    return jsonify({local_device_config["locked"]}), 200

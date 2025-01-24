from flask import Blueprint, jsonify, request
from sqlalchemy import select, insert, update, delete

from ...models import *
from ... import db

misc_blueprint = Blueprint("misc", __name__, url_prefix="")


@misc_blueprint.route("/unlock/", methods=["GET"])
def misc_handler():
    return jsonify({"endpoint": "GET_misc_handler"}), 500

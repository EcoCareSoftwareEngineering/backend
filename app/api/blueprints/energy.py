from flask import Blueprint, jsonify, request
from sqlalchemy import select, insert, update, delete

from ...models import *
from ... import db

energy_blueprint = Blueprint("energy", __name__, url_prefix="/energy")


@energy_blueprint.route("/", methods=["GET"])
def energy_handler():
    return jsonify({"endpoint": "GET_energy_handler"}), 500

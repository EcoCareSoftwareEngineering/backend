from flask import Blueprint, jsonify, request
from sqlalchemy import select, insert, update, delete

from ...models import *
from ... import db

goals_blueprint = Blueprint("goals", __name__, url_prefix="/goals")


@goals_blueprint.route("/", methods=["GET"])
def goals_handler():
    return jsonify({"endpoint": "GET_goals_handler"}), 500

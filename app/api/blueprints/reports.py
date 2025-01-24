from flask import Blueprint, jsonify, request
from sqlalchemy import select, insert, update, delete

from ...models import *
from ... import db

reports_blueprint = Blueprint("reports", __name__, url_prefix="/reports")


@reports_blueprint.route("/", methods=["GET"])
def reports_handler():
    return jsonify({"endpoint": "GET_reports_handler"}), 500

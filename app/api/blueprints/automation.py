from flask import Blueprint, jsonify, request
from sqlalchemy import select, insert, update, delete

from ...models import *
from ... import db

automations_blueprint = Blueprint("automations", __name__, url_prefix="/automations")


@automations_blueprint.route("/", methods=["GET", "POST"])
def automations_handler():
    if request.method == "GET":
        return get_automations_handler()
    elif request.method == "POST":
        return post_automations_handler()
    return jsonify({"Error": "Invalid"}), 500

#http://127.0.0.1:5000/api/automations/
def get_automations_handler():
    if request.args.get("deviceId") is None:
        statement = select(Automations)
    else:
        statement = select(Automations).where(Automations.deviceId == request.args.get("deviceId"))

    with db.engine.connect() as conn:
        results = conn.execute(statement)
    
    data_to_send = []
    for result in results:
        (
            automationId,
            deviceId,
            dateTime,
            newState,
        ) = result
    
        package = {
            "automationId": automationId,
            "deviceId": deviceId,
            "dateTime": dateTime,
            "newState": newState,
        }

        data_to_send.append(package)
    return jsonify(data_to_send), 200


def post_automations_handler():
    return jsonify({"endpoint": "POST_automations_handler"}), 200


@automations_blueprint.route("/<int:automation_id>/", methods=["PUT", "DELETE"])
def automations_update_handler(automation_id: int):
    if request.method == "GET":
        return put_automations_update_handler(automation_id)
    elif request.method == "POST":
        return delete_automations_update_handler(automation_id)
    return jsonify({"Error": "Invalid"}), 500


def put_automations_update_handler(automation_id: int):
    return jsonify({"endpoint": "PUT_automations_update_handler"}), 200


def delete_automations_update_handler(automation_id: int):
    return jsonify({"endpoint": "DELETE_automations_update_handler"}), 200

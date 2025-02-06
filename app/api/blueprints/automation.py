from flask import Blueprint, jsonify, request
from sqlalchemy import select, insert, update, delete
from jsonschema import *

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


# http://127.0.0.1:5000/api/automations/
def get_automations_handler():
    if request.args.get("deviceId") is None:
        statement = select(Automations)
    else:
        statement = select(Automations).where(
            Automations.deviceId == request.args.get("deviceId")
        )

    with db.engine.connect() as conn:
        results = conn.execute(statement)
    response = []
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

        response.append(package)
    return jsonify(response), 200


# curl -X POST -H "Content-Type: application/json" -d '{"deviceId": 2, "dateTime": "2000-03-15 23:20:30", "newState": [{"fieldName": "hue", "dataType": "integer", "value": 2}]}' http://127.0.0.1:5000/api/automations/
def post_automations_handler():
    jsonresult = request.json

    if jsonresult is None:
        return "", 500
    else:
        try:
            Validator.validate(
                jsonresult,
                {
                    "id": "auto",
                    "title": "Automation",
                    "description": "an automated action",
                    "type": "object",
                    "properties": {
                        "deviceId": {"type": "integer"},
                        "dateTime": {"type": "string"},
                        "newState": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "fieldName": {"type": "string"},
                                    "dataType": {"type": "string"},
                                    "value": {
                                        "oneOf": [
                                            {"type": "string"},
                                            {"type": "number"},
                                            {"type": "boolean"},
                                        ]
                                    },
                                },
                            },
                        },
                    },
                    "required": ["deviceId", "dateTime", "newState"],
                },
                cls=None,
            )
        except:
            return "", 500  # return error if we can't validate the json given

    statement = (
        insert(Automations)
        .values(
            deviceId=jsonresult["deviceId"],
            dateTime=jsonresult["dateTime"],
            newState=jsonresult[
                "newState"
            ],  # assuming the newState passed in is a dictionary
        )
        .returning(Automations.automationId)
    )

    with db.engine.connect() as conn:
        newId = conn.execute(statement).first()

        conn.commit()

    if newId is None:
        return "", 500

    statement = select(Automations).where(Automations.automationId == newId[0])
    with db.engine.connect() as conn:
        result = conn.execute(statement).first()

    if result is None:
        return "", 500

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

    return jsonify(package), 200


@automations_blueprint.route("/<int:automation_id>/", methods=["PUT", "DELETE"])
def automations_update_handler(automation_id: int):
    if request.method == "PUT":
        return put_automations_update_handler(automation_id)
    elif request.method == "DELETE":
        return delete_automations_update_handler(automation_id)
    return jsonify({"Error": "Invalid"}), 500


def put_automations_update_handler(automation_id: int):
    return jsonify({"endpoint": "PUT_automations_update_handler"}), 200


# curl -X DELETE http://127.0.0.1:5000/api/automations/28/
def delete_automations_update_handler(automation_id: int):
    statement = delete(Automations).where(Automations.automationId == automation_id)
    with db.engine.connect() as conn:
        results = conn.execute(statement)
        conn.commit()
    if results.rowcount > 0:  # if this has deleted anything return 200
        return "", 200
    else:  # if we failed to delete anything return 500
        return "", 500

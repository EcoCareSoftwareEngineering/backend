from flask import Blueprint, jsonify, request
from sqlalchemy import insert, select

from ...models import IotDevices, IotState
from ... import db

devices_blueprint = Blueprint("devices", __name__, url_prefix="/devices")


@devices_blueprint.route("/", methods=["GET", "POST"])
def devices_handler():
    if request.method == "GET":
        return get_devices_handler()
    elif request.method == "POST":
        statement = insert(IotDevices).values(
            name="Test", state={"State": "date"}, status=IotState.Ok
        )
        with db.engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return jsonify({"endpoint": "POST_devices_handler"}), 200
    return jsonify({"Error": "Invalid"}), 500


def get_devices_handler():
    statement = select(IotDevices)
    with db.engine.connect() as conn:
        data = conn.execute(statement)
        for row in data:
            print(row, flush=True)
    return jsonify({"endpoint": "GET_devices_handler"}), 200


@devices_blueprint.route("/new/", methods=["GET"])
def device_new_handler():
    return jsonify({"endpoint": "devices_new_handler"}), 200


@devices_blueprint.route("/<int:deviceId>/", methods=["PUT", "DELETE"])
def device_update_device_handler(deviceId: int):
    return (
        jsonify({"endpoint": "devices_update_device_handler", "deviceId": deviceId}),
        200,
    )


@devices_blueprint.route("/unlock/<int:deviceId>/", methods=["POST"])
def device_unlock_handler(deviceId: int):
    return jsonify({"endpoint": "devices_unlock_handler", "deviceId": deviceId}), 200

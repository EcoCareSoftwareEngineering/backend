from flask import Blueprint, jsonify, request
from flask_socketio import emit
from sqlalchemy import select, insert, update, delete

from ...models import *
from ... import db, socketio, unconnected_iot_devices
from ...routes import check_token
from ...websockets.events import send_iot_device_update
from jsonschema import *

devices_blueprint = Blueprint("devices", __name__, url_prefix="/devices")


@devices_blueprint.route("/", methods=["GET", "POST"])
def devices_handler():
    if request.method == "GET":
        return get_devices_handler()
    elif request.method == "POST":
        return post_devices_handler()
    return jsonify({"Error": "Invalid"}), 500


def get_devices_handler():
    if request.args.get("status") == "Fault":
        statement = select(IotDevices).where(
            IotDevices.status == IotDeviceFaultStatus.Fault
        )
    elif request.args.get("status") == "Ok":
        statement = select(IotDevices).where(
            IotDevices.status == IotDeviceFaultStatus.Ok
        )
    else:
        statement = select(IotDevices)

    with db.engine.connect() as conn:
        results = conn.execute(statement)

    data_to_send = []
    for result in results:
        (
            deviceId,
            name,
            description,
            state,
            status,
            faultStatus,
            pinCode,
            unlocked,
            uptimeTimestamp,
            ipAddress,
        ) = result

        # Data processing here

        entry = {
            "deviceId": deviceId,
            "name": name,
            "description": description,
            "state": state,
            "status": "On" if status == IotDeviceStatus.On else "Off",
            "faultStatus": "Ok" if faultStatus == IotDeviceFaultStatus.Ok else "Fault",
            "pinEnabled": pinCode is not None,
            "unlocked": unlocked,
            "uptimeTimestamp": uptimeTimestamp,
            "ipAddress": ipAddress,
        }
        data_to_send.append(entry)

    return jsonify(data_to_send), 200


def post_devices_handler():
    jsonresult = request.json
    if jsonresult is None:
        return "", 500
    else:
        try:
            validate(
                jsonresult,
                {
                    "properties": {
                        "ipAddress": {"type": "string"},
                    },
                    "required": ["ipAddress"],
                },
            )
        except:
            return "", 500
    response = []
    deletePos = -1
    for entry in unconnected_iot_devices:
        deletePos = deletePos + 1
        if entry["ipAddress"] == jsonresult["ipAddress"]:
            response.append(entry)
    if response != []:
        unconnected_iot_devices.pop(deletePos)
    return jsonify(response), 200


@devices_blueprint.route("/new/", methods=["GET"])
def devices_new_handler():
    return jsonify(unconnected_iot_devices), 200


@devices_blueprint.route("/<int:device_id>/", methods=["PUT", "DELETE"])
def devices_update_handler(device_id: int):
    if request.method == "PUT":
        return put_devices_update_handler(device_id)
    elif request.method == "DELETE":
        return delete_devices_update_handler(device_id)
    return jsonify({"Error": "Invalid"}), 500


def put_devices_update_handler(device_id: int):

    # After the DB has been updated, if there was an update call send_iot_device_update (used for spoof app communication)
    send_iot_device_update(device_id)

    return (
        jsonify({"endpoint": "PUT_devices_update_handler", "deviceId": device_id}),
        200,
    )


def delete_devices_update_handler(device_id: int):
    return (
        jsonify({"endpoint": "DELETE_devices_update_handler", "deviceId": device_id}),
        200,
    )


@devices_blueprint.route("/unlock/<int:device_id>/", methods=["POST"])
def devices_unlock_handler(device_id: int):
    return jsonify({"endpoint": "devices_unlock_handler", "deviceId": device_id}), 200


@devices_blueprint.route("/usage/", methods=["GET"])
def devices_usage_handler():
    return jsonify({"endpoint": "devices_usage_handler"}), 200

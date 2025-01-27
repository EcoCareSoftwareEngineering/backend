import ipaddress
import json
from flask import Blueprint, jsonify, request
from sqlalchemy import select, insert, update, delete

from ...models import *
from ... import db

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
        statement = select(IotDevices).where(IotDevices.status == IotState.Fault)
    elif request.args.get("status") == "Ok":
        statement = select(IotDevices).where(IotDevices.status == IotState.Ok)
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
            pinCode,
            unlocked,
            uptimeTimestamp,
            logPath,
            ipAddress,
            roomTag,
        ) = result

        # Data processing here

        entry = {
            "deviceId": deviceId,
            "name": name,
            "description": description,
            "state": state,
            "status": "Ok" if status == IotState.Ok else "Fault",
            "pinEnabled": pinCode is not None,
            "unlocked": unlocked,
            "uptimeTimestamp": uptimeTimestamp,
            "logPath": logPath,
            "ipAddress": ipAddress,
            "roomTag": roomTag,
        }
        data_to_send.append(entry)

    return jsonify(data_to_send), 200


def post_devices_handler():
    return jsonify({"endpoint": "POST_devices_handler"}), 200


@devices_blueprint.route("/new/", methods=["GET"])
def devices_new_handler():
    return jsonify({"endpoint": "devices_new_handler"}), 200


@devices_blueprint.route("/<int:device_id>/", methods=["PUT", "DELETE"])
def devices_update_handler(device_id: int):
    if request.method == "PUT":
        return put_devices_update_handler(device_id)
    elif request.method == "DELETE":
        return delete_devices_update_handler(device_id)
    return jsonify({"Error": "Invalid"}), 500


def put_devices_update_handler(device_id: int):
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

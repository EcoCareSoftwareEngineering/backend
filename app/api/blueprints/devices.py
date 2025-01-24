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
        return post_devices_handler()
        # statement = insert(IotDevices).values(
        #     name="Test", state={"State": "date"}, status=IotState.Ok
        # )
        # with db.engine.connect() as conn:
        #     conn.execute(statement)
        #     conn.commit()
        # return jsonify({"endpoint": "POST_devices_handler"}), 200
    return jsonify({"Error": "Invalid"}), 500


def get_devices_handler():
    # statement = select(IotDevices)
    # with db.engine.connect() as conn:
    #     data = conn.execute(statement)
    #     for row in data:
    #         print(row, flush=True)
    return jsonify({"endpoint": "GET_devices_handler"}), 200


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

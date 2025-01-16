from flask import Blueprint, jsonify, request
from ... import db

devices_blueprint = Blueprint("devices", __name__, url_prefix="/devices")


@devices_blueprint.route("/", methods=["GET", "POST"])
def devices_handler():
    if request.method == "GET":
        return jsonify({"endpoint": "GET_devices_handler"}), 200
    elif request.method == "POST":
        return jsonify({"endpoint": "POST_devices_handler"}), 200
    return jsonify({"Error": "Invalid"}), 500


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

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


# curl -X POST -H "Content-Type: application/json" -d '{"ipAddress": "192.168.0.10"}' http://127.0.0.1:5000/api/devices/
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

    deletePos = -1
    found = False
    for entry in unconnected_iot_devices:
        deletePos = deletePos + 1
        if entry["ipAddress"] == jsonresult["ipAddress"]:
            find = entry
            found = True
    if found:
        unconnected_iot_devices.pop(deletePos)
        response = []
        statement = (
            insert(IotDevices)
            .values(
                name=find["name"],
                description=find["description"],
                state=find["state"],
                status=find["status"],
                faultStatus=find["faultStatus"],
                ipAddress=find["ipAddress"],
            )
            .returning(IotDevices.deviceId)
        )
        with db.engine.connect() as conn:
            newId = conn.execute(statement).first()
            conn.commit()
        statement = select(IotDevices).where(IotDevices.deviceId == newId[0])
        with db.engine.connect() as conn:
            result = conn.execute(
                statement
            ).first()  # just to make sure we only get one even if something messes up

        if result is None:
            return "", 500

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

        package = {
            "deviceId": deviceId,
            "name": name,
            "description": description,
            "state": state,
            "status": "On" if status == IotDeviceStatus.On else "Off",
            "faultStatus": "Ok" if faultStatus == IotDeviceFaultStatus.Ok else "Fault",
            "pinCode": pinCode,
            "unlocked": unlocked,
            "uptimeTimestamp": uptimeTimestamp,
            "ipAddress": ipAddress,
        }

        return jsonify(package), 200
    else:
        return "", 500


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
    # jsonresult = request.json
    # if jsonresult is None:
    #     return "", 500
    # else:
    #     try:
    #         validate(
    #             jsonresult,
    #             {
    #                 "id": "devices",
    #                 "title": "device",
    #                 "description": "an iot Device",
    #                 "type": "object",
    #                 "properties": {
    #                     "name": {"type": "string"},
    #                     "description": {"type": "string"},
    #                     "state": {
    #                         "type": "array",
    #                         "items": {
    #                             "type": "object",
    #                             "properties": {
    #                                 "fieldName": {"type": "string"},
    #                                 "dataType": {"type": "string"},
    #                                 "value": {
    #                                     "oneOf": [
    #                                         {"type": "string"},
    #                                         {"type": "number"},
    #                                         {"type": "boolean"},
    #                                     ]
    #                                 },
    #                             },
    #                             "required": ["fieldName", "dataType", "value"],
    #                         },
    #                     },
    #                     "roomTag": {"type": "integer"},
    #                     "userTags": {
    #                         "type": "array",
    #                         "items": {
    #                             "type": "string",
    #                         },
    #                     },
    #                     "customTags": {
    #                         "type": "array",
    #                         "items": {
    #                             "type": "string",
    #                         },
    #                     },
    #                 },
    #             },
    #         )
    #     except:
    #         return "", 500
    #     if "name" in jsonresult:
    #         statement = (
    #             update(IotDevices)
    #             .where(IotDevices.deviceId == device_id)
    #             .values(name=jsonresult["name"])
    #         )
    #     if "description" in jsonresult:
    #         statement = (
    #             update(IotDevices)
    #             .where(IotDevices.deviceId == device_id)
    #             .values(name=jsonresult["description"])
    #         )
    #     if "state" in jsonresult:
    #         statement = (
    #             update(IotDevices)
    #             .where(IotDevices.deviceId == device_id)
    #             .values(name=jsonresult["state"])
    #         )
    #     #here I'm going to delete all the tags not in any of my tag lists before adding any
    #     statement = select(IotDevicesTags).where(
    #             IotDevicesTags.deviceId == device_id
    #         )
    #     with db.engine.connect() as conn:
    #         tagList = conn.execute(statement)
    #     for t in tagList:
    #         (
    #             device_id,
    #             tagId,
    #         ) = tagList
    #         deleteFlag = True
    #         if "userTags" in jsonresult:
    #             if jsonresult["userTags"].count(tagId) != 0: #we have this tagId in our usertag list
    #                 deleteFlag = True
    #         if "customTags" in jsonresult:
    #             if jsonresult["customTags"].count(tagId) != 0: #we have this tagId in our usertag list
    #                 deleteFlag = True
    #         if "roomTag" in jsonresult:
    #             if jsonresult["roomTag"] == tagId:
    #                 deleteFlag = True
    #         if not deleteFlag: #this tagId is not in any of our tag lists so it needs to be removed from the bridge table connecting this device to that tagid
    #             statement = delete(IotDevicesTags).where(IotDevicesTags.deviceId == device_id).where(IotDevicesTags.tagId == tagId)
    #             with db.engine.connect() as conn:
    #                 conn.execute(statement)
    #                 conn.commit()
    #     #now that we've removed all the tags that aren't in our taglists we can add any tags that aren't already inside
    #     if "userTags" in jsonresult:
    #         users = jsonresult["userTags"].copy()
    #         statement = select(IotDevicesTags).where(
    #             IotDevicesTags.deviceId == device_id
    #         )
    #         with db.engine.connect() as conn:
    #             tagList = conn.execute(statement)
    #         for t in tagList:
    #             (
    #                 device_id,
    #                 tagId,
    #             ) = tagList
    #             if jsonresult["userTags"].count(tagId) == 0: #we don't have this tagId in our new list
    #                 if "customTags" in jsonresult:

    #         statement = (
    #             update(IotDevices)
    #             .where(IotDevices.deviceId == device_id)
    #             .values(name=jsonresult[""])
    #         )

    # # After the DB has been updated, if there was an update call send_iot_device_update (used for spoof app communication)
    # send_iot_device_update(device_id)
    # return (
    #     jsonify({"endpoint": "PUT_devices_update_handler", "deviceId": device_id}),
    #     200,
    # )

    # After the DB has been updated, if there was an update call send_iot_device_update (used for spoof app communication)
    send_iot_device_update(device_id)

    return (
        jsonify({"endpoint": "PUT_devices_update_handler", "deviceId": device_id}),
        200,
    )


def delete_devices_update_handler(device_id: int):
    # remove all automations, device usage and tag connections to this device
    statement = delete(Automations).where(Automations.deviceId == device_id)
    with db.engine.connect() as conn:
        conn.execute(statement)
        conn.commit()
    statement = delete(IotDeviceUsage).where(IotDeviceUsage.deviceId == device_id)
    with db.engine.connect() as conn:
        conn.execute(statement)
        conn.commit()
    statement = delete(IotDevicesTags).where(IotDevicesTags.deviceId == device_id)
    with db.engine.connect() as conn:
        conn.execute(statement)
        conn.commit()
    # now we can delete the device
    statement = delete(IotDevices).where(IotDevices.deviceId == device_id)
    with db.engine.connect() as conn:
        results = conn.execute(statement)
        conn.commit()
    if results.rowcount > 0:
        return "", 200
    else:
        return "", 500


@devices_blueprint.route("/unlock/<int:device_id>/", methods=["POST"])
def devices_unlock_handler(device_id: int):
    # check if pinenabled
    jsonresult = request.json
    if jsonresult is None:
        return "", 500
    else:
        try:
            validate(
                jsonresult,
                {
                    "properties": {
                        "pin": {"type": "string"},
                    },
                    "required": ["pin"],
                },
            )
        except:
            return "", 500
    statement = select(IotDevices).where(IotDevices.deviceId == device_id)
    with db.engine.connect() as conn:
        result = conn.execute(statement).first()
    if result is None:
        return "", 500
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

    if pinCode == jsonresult["pin"]:  # passcode is correct! set device to be unlocked
        statement = (
            update(IotDevices)
            .where(IotDevices.deviceId == device_id)
            .values(unlocked=True)
        )
        with db.engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "", 200
    return "", 500


@devices_blueprint.route("/usage/", methods=["GET"])
def devices_usage_handler():
    return jsonify({"endpoint": "devices_usage_handler"}), 200

from flask import Blueprint, jsonify, request
from sqlalchemy import distinct, select, insert, update, delete, func, text
from datetime import datetime, timedelta

from ...models import *
from ... import db, unconnected_iot_devices
from ...routes import check_authentication
from ...websockets.events import send_iot_device_update
from jsonschema import *

devices_blueprint = Blueprint("devices", __name__, url_prefix="/devices")


@devices_blueprint.route("/", methods=["GET", "POST"])
@check_authentication
def devices_handler():
    if request.method == "GET":
        return get_devices_handler()
    elif request.method == "POST":
        return post_devices_handler()
    return jsonify({"Error": "Invalid"}), 500


def get_devices_handler():
    statement = select(IotDevices)

    device_id = request.args.get("deviceId")
    if device_id is not None:
        statement = statement.where(IotDevices.deviceId == device_id)

    name = request.args.get("name")
    if name is not None:
        statement = statement.where(IotDevices.name == name)

    status = request.args.get("status")
    if status is not None:
        statement = statement.where(
            IotDevices.status
            == (IotDeviceStatus.On if status == "On" else IotDeviceStatus.Off)
        )

    fault_status = request.args.get("faultStatus")
    if fault_status is not None:
        statement = statement.where(
            IotDevices.faultStatus
            == (
                IotDeviceFaultStatus.Ok
                if status == "Ok"
                else IotDeviceFaultStatus.Fault
            )
        )

    roomTag = request.args.get("roomTag")
    if roomTag is not None:
        tags_statement = select(IotDevicesTags.deviceId).where(
            IotDevicesTags.tagId == roomTag
        )

        with db.engine.connect() as conn:
            results = conn.execute(tags_statement)

        ids = [result[0] for result in results]

        statement = statement.where(IotDevices.deviceId.in_(ids))

    userTag = request.args.get("userTag")
    if userTag is not None:
        tags_statement = select(IotDevicesTags.deviceId).where(
            IotDevicesTags.tagId == userTag
        )

        with db.engine.connect() as conn:
            results = conn.execute(tags_statement)

        ids = [result[0] for result in results]

        statement = statement.where(IotDevices.deviceId.in_(ids))

    customTag = request.args.get("customTag")
    if customTag is not None:
        tags_statement = select(IotDevicesTags.deviceId).where(
            IotDevicesTags.tagId == customTag
        )

        with db.engine.connect() as conn:
            results = conn.execute(tags_statement)

        ids = [result[0] for result in results]

        statement = statement.where(IotDevices.deviceId.in_(ids))

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

        statement = (
            select(Tags.tagId, Tags.tagType)
            .join(IotDevicesTags, Tags.tagId == IotDevicesTags.tagId)
            .join(IotDevices, IotDevices.deviceId == IotDevicesTags.deviceId)
            .where(IotDevices.deviceId == deviceId)
        )

        roomTag = None
        userTags = []
        customTags = []

        with db.engine.connect() as conn:
            results = conn.execute(statement)

        for result in results:
            (tag_id, tag_type) = result
            if tag_type == TagType.Room:
                roomTag = tag_id
            if tag_type == TagType.User:
                userTags.append(tag_id)
            if tag_type == TagType.Custom:
                customTags.append(tag_id)

        entry = {
            "deviceId": deviceId,
            "name": name,
            "description": description,
            "state": state,
            "status": "On" if status == IotDeviceStatus.On else "Off",
            "faultStatus": "Ok" if faultStatus == IotDeviceFaultStatus.Ok else "Fault",
            "pinEnabled": pinCode != "None",
            "unlocked": unlocked,
            "uptimeTimestamp": uptimeTimestamp,
            "ipAddress": ipAddress,
            "roomTag": roomTag,
            "userTags": userTags,
            "customTags": customTags,
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
                pinCode="None",
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

        send_iot_device_update(deviceId)

        return jsonify(package), 200
    else:
        return "", 500


@devices_blueprint.route("/new/", methods=["GET"])
@check_authentication
def devices_new_handler():
    return jsonify(unconnected_iot_devices), 200


@devices_blueprint.route("/<int:device_id>/", methods=["PUT", "DELETE"])
@check_authentication
def devices_update_handler(device_id: int):
    if request.method == "PUT":
        return put_devices_update_handler(device_id)
    elif request.method == "DELETE":
        return delete_devices_update_handler(device_id)
    return jsonify({"Error": "Invalid"}), 500


def put_devices_update_handler(device_id: int):
    json = request.json
    if json is None:
        return jsonify({}), 500

    select_statement = select(IotDevices.unlocked).where(
        IotDevices.deviceId == device_id
    )

    with db.engine.connect() as conn:
        result = conn.execute(select_statement).first()

    if result is None:
        return jsonify({"Error": "Device not found"}), 500

    result = result[0]

    if not result:
        return jsonify({"Error": "Device locked"}), 500

    values = {}

    if "name" in json:
        values["name"] = json["name"]
    if "description" in json:
        values["description"] = json["description"]
    if "state" in json:
        values["state"] = json["state"]
    if "status" in json:
        status_value = (
            IotDeviceStatus.On if json["status"] == "On" else IotDeviceStatus.Off
        )
        values["status"] = status_value

    update_statement = (
        update(IotDevices).where(IotDevices.deviceId == device_id).values(**values)
    )
    delete_tags_statement = delete(IotDevicesTags).where(
        IotDevicesTags.deviceId == device_id
    )

    room_tag = None

    statement = select(IotDevicesTags.tagId).where(IotDevicesTags.deviceId == device_id)
    with db.engine.connect() as conn:
        result = conn.execute(statement).first()

    if result is not None:
        room_tag = result[0]

    rows = []
    if "roomTag" in json:
        rows.append({"deviceId": device_id, "tagId": int(json["roomTag"])})
    elif room_tag is not None:
        rows.append({"deviceId": device_id, "tagId": int(room_tag)})
    if "userTag" in json:
        rows.extend(
            {"deviceId": device_id, "tagId": int(tag_id)} for tag_id in json["userTag"]
        )
    if "customTag" in json:
        rows.extend(
            {"deviceId": device_id, "tagId": int(tag_id)}
            for tag_id in json["customTag"]
        )

    with db.engine.connect() as conn:
        if values != {}:
            conn.execute(update_statement)
        conn.execute(delete_tags_statement)
        if rows != []:
            conn.execute(insert(IotDevicesTags), rows)
        conn.commit()

    # After the DB has been updated, if there was an update call send_iot_device_update (used for spoof app communication)
    send_iot_device_update(device_id)

    statement = select(IotDevices).where(IotDevices.deviceId == device_id)

    with db.engine.connect() as conn:
        result = conn.execute(statement).first()

    if result is None:
        return jsonify({}), 500

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

    statement = (
        select(Tags.tagId, Tags.tagType)
        .join(IotDevicesTags, Tags.tagId == IotDevicesTags.tagId)
        .join(IotDevices, IotDevices.deviceId == IotDevicesTags.deviceId)
        .where(IotDevices.deviceId == deviceId)
    )

    roomTag = None
    userTags = []
    customTags = []

    with db.engine.connect() as conn:
        results = conn.execute(statement)

    for result in results:
        (tag_id, tag_type) = result
        if tag_type == TagType.Room:
            roomTag = tag_id
        if tag_type == TagType.User:
            userTags.append(tag_id)
        if tag_type == TagType.Custom:
            customTags.append(tag_id)

    response = {
        "deviceId": deviceId,
        "name": name,
        "description": description,
        "state": state,
        "status": "On" if status == IotDeviceStatus.On else "Off",
        "faultStatus": "Ok" if faultStatus == IotDeviceFaultStatus.Ok else "Fault",
        "pinEnabled": pinCode != "None",
        "unlocked": unlocked,
        "uptimeTimestamp": uptimeTimestamp,
        "ipAddress": ipAddress,
        "roomTag": roomTag,
        "userTags": userTags,
        "customTags": customTags,
    }

    return jsonify(response), 200


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


# curl -X POST -H "Content-Type: application/json" -d '{"pin": "1234"}' http://127.0.0.1:5000/api/devices/unlock/6/
# ^ change entry 6 in iot_devices.csv to have a pincode and unlocked = false before using this
@devices_blueprint.route("/unlock/<int:device_id>/", methods=["POST"])
@check_authentication
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
@check_authentication
def devices_usage_handler():
    start_date = request.args.get("rangeStart")
    end_date = request.args.get("rangeEnd")
    device_id = request.args.get("deviceId")
    time_period = request.args.get("timePeriod", "hourly")

    if start_date is None or end_date is None:
        return jsonify({"Error": "Missing required fields: rangeStart, rangeEnd"}), 400

    try:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        end_datetime = end_datetime.replace(hour=0, minute=0, second=0)
    except ValueError:
        return jsonify({"Error": "Invalid date format. Use YYYY-MM-DD"}), 400

    # Validate time_period
    allowed_periods = {"hourly", "daily", "monthly"}
    if time_period not in allowed_periods:
        return (
            jsonify(
                {"Error": f"Invalid timePeriod. Must be one of: {allowed_periods}"}
            ),
            400,
        )

    # Define grouping logic and generate all time periods
    all_timestamps = []
    format_string = ""

    if time_period == "hourly":
        time_group = func.date_format(IotDeviceUsage.datetime, "%Y-%m-%d %H:00:00")
        format_string = "%Y-%m-%d %H:00:00"
        delta = timedelta(hours=1)
        current = start_datetime.replace(minute=0, second=0, microsecond=0)

    elif time_period == "daily":
        time_group = func.date_format(IotDeviceUsage.datetime, "%Y-%m-%d 00:00:00")
        format_string = "%Y-%m-%d"
        delta = timedelta(days=1)
        current = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

    elif time_period == "monthly":
        time_group = func.date_format(IotDeviceUsage.datetime, "%Y-%m-01 00:00:00")
        format_string = "%Y-%m"
        current = start_datetime.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )

    while current < end_datetime:
        all_timestamps.append(current.strftime(format_string))
        if time_period == "monthly":
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1)
            else:
                current = current.replace(month=current.month + 1)
        else:
            current += delta

    if device_id:
        device_ids = [device_id]
    else:
        device_query = select(distinct(IotDeviceUsage.deviceId))
        with db.engine.connect() as conn:
            device_ids = [row[0] for row in conn.execute(device_query).fetchall()]

    statement = (
        select(
            IotDeviceUsage.deviceId,
            time_group.label("time_period"),
            func.sum(IotDeviceUsage.usage).label("usage"),
        )
        .where(
            (IotDeviceUsage.datetime >= start_datetime)
            & (IotDeviceUsage.datetime <= end_datetime)
        )
        .group_by(IotDeviceUsage.deviceId, "time_period")
        .order_by("time_period")
    )

    if device_id:
        try:
            device_id = int(device_id)
            device_ids = [device_id]
            statement = statement.where(IotDeviceUsage.deviceId == device_id)
        except ValueError:
            return jsonify({"Error": "Device ID must be a number"}), 400

    with db.engine.connect() as conn:
        results = conn.execute(statement).fetchall()

    usage_dict = {}  #
    for result_device_id, time_str, usage in results:
        if time_period == "monthly":
            formatted_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").strftime(
                "%Y-%m"
            )
        elif time_period == "daily":
            formatted_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").strftime(
                "%Y-%m-%d"
            )
        else:
            formatted_time = time_str

        if result_device_id not in usage_dict:
            usage_dict[result_device_id] = {}

        usage_dict[result_device_id][formatted_time] = (
            float(usage) if usage is not None else usage
        )

    response = []
    for current_device_id in device_ids:
        usage_list = [
            {
                "datetime": timestamp,
                "usage": usage_dict.get(current_device_id, {}).get(timestamp, 0.0),
            }
            for timestamp in all_timestamps
        ]
        response.append({"deviceId": current_device_id, "usage": usage_list})

    return jsonify(response), 200

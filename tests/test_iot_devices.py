import copy
from datetime import datetime
import requests


def test_get_iot_devices(login, iot_devices_data, iot_devices_tags_data, tags_data):
    response = requests.get(
        "http://127.0.0.1:5000/api/devices/", headers={"token": login}
    ).json()

    for device in iot_devices_data:
        roomTag = None
        userTags = []
        customTags = []

        for tag in iot_devices_tags_data:
            if tag["deviceId"] != device["deviceId"]:
                continue

            for other_tag in tags_data:
                if other_tag["tagId"] != tag["tagId"]:
                    continue

                if other_tag["tagType"] == "Room":
                    roomTag = tag["tagId"]
                elif other_tag["tagType"] == "User":
                    userTags.append(tag["tagId"])
                elif other_tag["tagType"] == "Custom":
                    customTags.append(tag["tagId"])

        device["roomTag"] = roomTag
        device["userTags"] = userTags
        device["customTags"] = customTags

    assert response == iot_devices_data


def test_put_iot_devices(login, iot_devices_data, iot_devices_tags_data, tags_data):
    for device in iot_devices_data:
        roomTag = None
        userTags = []
        customTags = []

        for tag in iot_devices_tags_data:
            if tag["deviceId"] != device["deviceId"]:
                continue

            for other_tag in tags_data:
                if other_tag["tagId"] != tag["tagId"]:
                    continue

                if other_tag["tagType"] == "Room":
                    roomTag = tag["tagId"]
                elif other_tag["tagType"] == "User":
                    userTags.append(tag["tagId"])
                elif other_tag["tagType"] == "Custom":
                    customTags.append(tag["tagId"])

        device["roomTag"] = roomTag
        device["userTags"] = userTags
        device["customTags"] = customTags

    devices = copy.deepcopy(iot_devices_data)

    device = devices[0]

    update = {"state": [{"datatype": "integer", "fieldName": "hue", "value": 3}]}
    device["state"] = [{"datatype": "integer", "fieldName": "hue", "value": 3}]

    response = requests.put(
        "http://127.0.0.1:5000/api/devices/1/", json=update, headers={"token": login}
    ).json()
    assert response == device

    response = requests.get(
        "http://127.0.0.1:5000/api/devices/", headers={"token": login}
    ).json()
    assert response == devices


def test_add_new_iot_device(login, iot_devices_data):
    unconnected_iot_devices = [
        {
            "ipAddress": "192.168.0.11",
            "name": "Smart Light",
            "description": "A smart lightbulb",
            "state": [],
            "status": "On",
            "faultStatus": "Ok",
        },
        {
            "ipAddress": "192.168.0.12",
            "name": "Smart Lock",
            "description": "A smart lock",
            "state": [{"fieldName": "engaged", "datatype": "boolean", "value": True}],
            "status": "On",
            "faultStatus": "Ok",
        },
    ]

    assert (
        unconnected_iot_devices
        == requests.get(
            "http://127.0.0.1:5000/api/devices/new/", headers={"token": login}
        ).json()
    )

    assert (
        200
        == requests.post(
            "http://127.0.0.1:5000/api/devices/",
            headers={"token": login},
            json={"ipAddress": "192.168.0.11"},
        ).status_code
    )

    devices = iot_devices_data.copy()
    devices.append(
        {
            "ipAddress": "192.168.0.11",
            "name": "Smart Light",
            "description": "A smart lightbulb",
            "state": [],
            "status": "On",
            "faultStatus": "Ok",
            "customTags": [],
            "deviceId": 8,
            "faultStatus": "Ok",
            "pinEnabled": False,
            "roomTag": None,
            "uptimeTimestamp": None,
            "unlocked": None,
            "userTags": [],
        }
    )
    assert (
        devices
        == requests.get(
            "http://127.0.0.1:5000/api/devices/", headers={"token": login}
        ).json()
    )


def test_delete_iot_devices(login, iot_devices_data, iot_devices_tags_data, tags_data):
    for device in iot_devices_data:
        roomTag = None
        userTags = []
        customTags = []

        for tag in iot_devices_tags_data:
            if tag["deviceId"] != device["deviceId"]:
                continue

            for other_tag in tags_data:
                if other_tag["tagId"] != tag["tagId"]:
                    continue

                if other_tag["tagType"] == "Room":
                    roomTag = tag["tagId"]
                elif other_tag["tagType"] == "User":
                    userTags.append(tag["tagId"])
                elif other_tag["tagType"] == "Custom":
                    customTags.append(tag["tagId"])

        device["roomTag"] = roomTag
        device["userTags"] = userTags
        device["customTags"] = customTags

    response = requests.delete(
        "http://127.0.0.1:5000/api/devices/1/", headers={"token": login}
    )
    assert response.status_code == 200

    devices = iot_devices_data.copy()

    devices.pop(0)

    response = requests.get(
        "http://127.0.0.1:5000/api/devices/", headers={"token": login}
    ).json()
    assert response == devices


def test_unlock_iot_device(login, iot_devices_data, iot_devices_tags_data, tags_data):
    for device in iot_devices_data:
        roomTag = None
        userTags = []
        customTags = []

        for tag in iot_devices_tags_data:
            if tag["deviceId"] != device["deviceId"]:
                continue

            for other_tag in tags_data:
                if other_tag["tagId"] != tag["tagId"]:
                    continue

                if other_tag["tagType"] == "Room":
                    roomTag = tag["tagId"]
                elif other_tag["tagType"] == "User":
                    userTags.append(tag["tagId"])
                elif other_tag["tagType"] == "Custom":
                    customTags.append(tag["tagId"])

        device["roomTag"] = roomTag
        device["userTags"] = userTags
        device["customTags"] = customTags

    devices = iot_devices_data.copy()

    devices[1]["unlocked"] = True

    response = requests.post(
        "http://127.0.0.1:5000/api/devices/unlock/2/",
        json={"pin": "1234"},
        headers={"token": login},
    )
    assert response.status_code == 200

    response = requests.get(
        "http://127.0.0.1:5000/api/devices/", headers={"token": login}
    ).json()
    assert response == devices


def test_iot_devices_usage(login, iot_device_usage_data):
    usages = []
    ids = []

    for usage in iot_device_usage_data:
        if usage["deviceId"] not in ids:
            ids.append(usage["deviceId"])
            usages.append({"deviceId": usage["deviceId"], "usage": []})

        for entry in usages:
            if entry["deviceId"] == usage["deviceId"]:
                entry["usage"].append(
                    {
                        "datetime": usage["datetime"],
                        "usage": usage["usage"],
                    }
                )

    response = requests.get(
        "http://127.0.0.1:5000/api/devices/usage/?rangeStart=2025-01-01&rangeEnd=2025-02-01",
        headers={"token": login},
    ).json()

    for record in response:
        for entry in record["usage"]:
            entry["datetime"] = datetime.strptime(
                entry["datetime"], "%a, %d %b %Y %H:%M:%S GMT"
            )

    assert response == usages

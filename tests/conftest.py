import csv
from datetime import datetime
import json
import pytest
import requests
from app.models import TagType


@pytest.fixture(scope="session")
def login():
    response = requests.post(
        "http://127.0.0.1:5000/api/accounts/login/",
        json={"username": "testing", "password": "testing123"},
    ).json()

    return response["token"]


@pytest.fixture(autouse=True, scope="function")
def config():
    response = requests.post("http://127.0.0.1:5000/dev/resetdb/").json()
    assert response == ""
    yield


@pytest.fixture(scope="session")
def automations_data():
    rows = []
    with open("data/automations.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        rows.extend([row for row in reader])

    data = []
    for row in rows:
        row["automationId"] = int(row["automationId"])
        row["deviceId"] = int(row["deviceId"])
        row["newState"] = json.loads(row["newState"])
        data.append({key: value for key, value in row.items() if value != ""})

    data[0]["dateTime"] = "Sun, 02 Feb 2025 08:00:00 GMT"
    data[1]["dateTime"] = "Sun, 02 Feb 2025 09:00:00 GMT"

    return data


@pytest.fixture(scope="session")
def energy_records_data():
    rows = []
    with open("data/energy_records.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        rows.extend([row for row in reader])

    data = []
    for row in rows:
        del row["energyRecordId"]
        row["energyUse"] = float(row["energyUse"])
        row["energyGeneration"] = float(row["energyGeneration"])
        row["datetime"] = datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M:%S")
        data.append({key: value for key, value in row.items() if value != ""})

    return data


@pytest.fixture(scope="session")
def energy_saving_goals_data():
    rows = []
    with open("data/energy_saving_goals.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        rows.extend([row for row in reader])

    data = []
    for row in rows:
        row["goalId"] = int(row["goalId"])
        row["target"] = float(row["target"])
        row["progress"] = float(row["progress"])
        row["complete"] = row["complete"] == "True"
        data.append({key: value for key, value in row.items() if value != ""})

    data[0]["date"] = "Wed, 02 Apr 2025 00:00:00 GMT"
    data[1]["date"] = "Wed, 02 Apr 2025 00:00:00 GMT"

    return data


@pytest.fixture(scope="session")
def iot_device_usage_data():
    rows = []
    with open("data/iot_device_usage.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        rows.extend([row for row in reader])

    data = []
    for row in rows:
        row["deviceUsageId"] = int(row["deviceUsageId"])
        row["usage"] = int(row["usage"])
        row["datetime"] = datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M:%S")
        row["deviceId"] = int(row["deviceId"]) if row["deviceId"] else None
        data.append({key: value for key, value in row.items() if value != ""})

    return data


@pytest.fixture(scope="session")
def iot_devices_tags_data():
    rows = []
    with open("data/iot_devices_tags.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        rows.extend([row for row in reader])

    data = []
    for row in rows:
        row["deviceId"] = int(row["deviceId"])
        row["tagId"] = int(row["tagId"])
        data.append({key: value for key, value in row.items() if value != ""})

    return data


@pytest.fixture(scope="session")
def iot_devices_data():
    rows = []
    with open("data/iot_devices.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        rows.extend([row for row in reader])

    data = []
    for row in rows:
        row["state"] = json.loads(row["state"])
        for entry in row["state"]:
            if entry["datatype"] == "integer":
                entry["value"] = int(entry["value"])
            if entry["datatype"] == "float":
                entry["value"] = float(entry["value"])

        entry = {
            "deviceId": int(row["deviceId"]),
            "name": row["name"],
            "description": row["description"],
            "state": row["state"],
            "status": row["status"],
            "faultStatus": row["faultStatus"],
            "pinEnabled": row["pinCode"] != "None",
            "unlocked": row["unlocked"] == "True",
            "uptimeTimestamp": row["uptimeTimestamp"] or None,
            "ipAddress": row["ipAddress"],
        }
        data.append(entry)

    return data


@pytest.fixture(scope="session")
def tags_data():
    rows = []
    with open("data/tags.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        rows.extend([row for row in reader])

    data = []
    for row in rows:
        row["tagId"] = int(row["tagId"])
        row["tagType"] = TagType[row["tagType"]].name
        data.append({key: value for key, value in row.items() if value != ""})

    return data


@pytest.fixture(scope="session")
def users_data():
    rows = []
    with open("data/users.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        rows.extend([row for row in reader])

    data = []
    for row in rows:
        row["userId"] = int(row["userId"])
        data.append({key: value for key, value in row.items() if value != ""})

    return data

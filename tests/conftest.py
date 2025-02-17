import csv
import json
import pytest
import requests
from app.models import TagType


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
        row["energyRecordId"] = int(row["energyRecordId"])
        row["hour"] = int(row["hour"])
        row["energyUse"] = float(row["energyUse"])
        row["energyGeneration"] = float(row["energyGeneration"])
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
        row["target"] = float(row["goalId"])
        row["progress"] = float(row["progress"])
        row["complete"] = bool(row["complete"])
        data.append({key: value for key, value in row.items() if value != ""})

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
        row["hour"] = int(row["hour"])
        row["usage"] = int(row["usage"])
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
            "pinEnabled": row["pinCode"] != "",
            "unlocked": bool(row["unlocked"]),
            "uptimeTimestamp": row["uptimeTimestamp"],
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

import csv
import json
import pytest
import requests


@pytest.fixture(autouse=True, scope="function")
def config():
    response = requests.post("http://127.0.0.1:5000/dev/resetdb/").json()
    assert response == ""
    yield


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

        entry = {
            "deviceId": int(row["deviceId"]),
            "name": row["name"],
            "description": row["description"],
            "state": row["state"],
            "status": row["status"],
            "faultStatus": row["faultStatus"],
            "pinEnabled": row["pinCode"] != "",
            "unlocked": bool(row["unlocked"]),
            "uptimeTimestamp": (
                row["uptimeTimestamp"] if "uptimeTimestamp" in row else None
            ),
            "ipAddress": row["ipAddress"] if "ipAddress" in row else None,
        }
        data.append(entry)

    return data


# TODO add other fixtures for every csv file - copy code from data.py

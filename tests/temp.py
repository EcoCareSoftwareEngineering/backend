import csv, json

rows = []
with open("data/iot_devices.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    rows.extend([row for row in reader])

data = []
for row in rows:
    print(row["state"])
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

print(data)

from sqlalchemy import select, insert, text, update, delete
import csv, json

from . import db
from .models import *


def reset_db():
    delete_data_from_db()
    add_data()


def delete_data_from_db():
    with db.engine.connect() as conn:
        conn.execute(delete(IotDevices))
        conn.execute(text("ALTER TABLE iot_devices AUTO_INCREMENT = 0;"))

        # TODO Finish deleting data
        # TODO Reset autoincrement values to 0

        conn.commit()


def add_data():
    with db.engine.connect() as conn:

        rows = []
        with open("data/iot_devices.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            rows.extend([row for row in reader])

        data = []
        for row in rows:
            row["deviceId"] = int(row["deviceId"])
            row["state"] = json.loads(row["state"])
            for entry in row["state"]:
                if entry["datatype"] == "integer":
                    entry["value"] = int(entry["value"])
            row["unlocked"] = bool(row["unlocked"])

            data.append({key: value for key, value in row.items() if value != ""})

        # TODO Add data to rest of tables

        conn.execute(insert(IotDevices), data)
        conn.commit()


def add_data_check():
    with db.engine.connect() as conn:
        result = conn.execute(select(Initialised)).first()

    if result is None:
        add_data()
        with db.engine.connect() as conn:
            conn.execute(insert(Initialised))
            conn.commit()

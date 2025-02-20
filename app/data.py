from sqlalchemy import select, insert, text, update, delete
import csv, json
import datetime as datetime

from . import db
from .models import *


def reset_db():
    delete_data_from_db()
    add_data()


def delete_data_from_db():
    with db.engine.connect() as conn:
        conn.execute(delete(IotDevicesTags))
        conn.execute(text("ALTER TABLE iot_devices_tags AUTO_INCREMENT = 0;"))
        conn.execute(delete(IotDeviceUsage))
        conn.execute(text("ALTER TABLE iot_device_usage AUTO_INCREMENT = 0;"))
        conn.execute(delete(Automations))
        conn.execute(text("ALTER TABLE automations AUTO_INCREMENT = 0;"))
        conn.execute(delete(IotDevices))
        conn.execute(text("ALTER TABLE iot_devices AUTO_INCREMENT = 0;"))
        conn.execute(delete(Tags))
        conn.execute(text("ALTER TABLE tags AUTO_INCREMENT = 0;"))
        conn.execute(delete(EnergySavingGoals))
        conn.execute(text("ALTER TABLE energy_saving_goals AUTO_INCREMENT = 0;"))
        conn.execute(delete(EnergyRecords))
        conn.execute(text("ALTER TABLE energy_records AUTO_INCREMENT = 0;"))
        conn.execute(delete(Users))
        conn.execute(text("ALTER TABLE users AUTO_INCREMENT = 0;"))
        conn.commit()


def add_data():
    with db.engine.connect() as conn:

        # Data for iot_devices
        device_rows = []
        try:
            with open("data/iot_devices.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                device_rows.extend([row for row in reader])
        except Exception as e:
            print(f"Error reading CSV file 'iot_devices.csv' with error: {e}")

        device_data = []
        for row in device_rows:
            row["deviceId"] = int(row["deviceId"])
            row["state"] = json.loads(row["state"])
            for entry in row["state"]:
                if entry["datatype"] == "integer":
                    entry["value"] = int(entry["value"])
                elif entry["datatype"] == "float":
                    entry["value"] = float(entry["value"])
                elif entry["datatype"] == "boolean":
                    entry["value"] = bool(entry["value"])
            row["unlocked"] = row["unlocked"] == "True"

            device_data.append(
                {key: value for key, value in row.items() if value != ""}
            )
        print(device_rows, flush=True)
        print(device_data, flush=True)
        conn.execute(insert(IotDevices), device_data)

        # Data for tags
        tag_rows = []
        try:
            with open("data/tags.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                tag_rows.extend([row for row in reader])
        except Exception as e:
            print(f"Error reading CSV file 'tags.csv' with error: {e}")

        tag_data = []
        for row in tag_rows:
            row["tagId"] = int(row["tagId"])
            row["tagType"] = TagType[row["tagType"]]
            tag_data.append({key: value for key, value in row.items() if value != ""})

        conn.execute(insert(Tags), tag_data)

        # Data for IotDevicesTags (device and tag)
        device_tag_rows = []
        try:
            with open("data/iot_devices_tags.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                device_tag_rows.extend([row for row in reader])
        except Exception as e:
            print(f"Error reading CSV file 'iot_device_tags.csv' with error {e}")

        device_tag_data = []
        for row in device_tag_rows:
            row["deviceId"] = int(row["deviceId"])
            row["tagId"] = int(row["tagId"])
            device_tag_data.append(
                {key: value for key, value in row.items() if value != ""}
            )

        conn.execute(insert(IotDevicesTags), device_tag_data)

        # Data for IotDeviceUsage
        device_usage_rows = []
        try:
            with open("data/iot_device_usage.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                device_usage_rows.extend([row for row in reader])
        except Exception as e:
            print(f"Error reading CSV file 'iot_device_usage.csv' with error {e}")

        device_usage_data = []
        for row in device_usage_rows:
            row["deviceUsageId"] = int(row["deviceUsageId"])
            row["hour"] = int(row["hour"])
            row["usage"] = int(row["usage"])
            row["deviceId"] = int(row["deviceId"]) if row["deviceId"] else None
            device_usage_data.append(
                {key: value for key, value in row.items() if value != ""}
            )

        conn.execute(insert(IotDeviceUsage), device_usage_data)

        # Data for Automations
        automation_rows = []
        try:
            with open("data/automations.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                automation_rows.extend([row for row in reader])
        except Exception as e:
            print(f"Error reading CSV file 'automations.csv' with error {e}")

        automation_data = []
        for row in automation_rows:
            row["automationId"] = int(row["automationId"])
            row["deviceId"] = int(row["deviceId"])
            row["newState"] = json.loads(row["newState"])
            automation_data.append(
                {key: value for key, value in row.items() if value != ""}
            )

        conn.execute(insert(Automations), automation_data)

        # Data for EnergySavingGoals
        energy_saving_goal_rows = []
        try:
            with open("data/energy_saving_goals.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                energy_saving_goal_rows.extend([row for row in reader])
        except Exception as e:
            print(f"Error reading CSV file 'energy_saving_goals.csv' with error {e}")

        energy_saving_goal_data = []
        for row in energy_saving_goal_rows:
            row["goalId"] = int(row["goalId"])
            row["target"] = float(row["goalId"])
            row["progress"] = float(row["progress"])
            row["complete"] = bool(row["complete"])
            energy_saving_goal_data.append(
                {key: value for key, value in row.items() if value != ""}
            )

        conn.execute(insert(EnergySavingGoals), energy_saving_goal_data)

        # Data for EnergyRecotds
        energy_record_rows = []
        try:
            with open("data/energy_records.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                energy_record_rows.extend([row for row in reader])
        except Exception as e:
            print(f"Error reading CSV file 'energy_records.csv' with error {e}")

        energy_record_data = []
        for row in energy_record_rows:
            row["energyRecordId"] = int(row["energyRecordId"])
            row["hour"] = int(row["hour"])
            row["energyUse"] = float(row["energyUse"])
            row["energyGeneration"] = float(row["energyGeneration"])
            energy_record_data.append(
                {key: value for key, value in row.items() if value != ""}
            )

        conn.execute(insert(EnergyRecords), energy_record_data)

        # Data for Users
        user_rows = []
        try:
            with open("data/users.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                user_rows.extend([row for row in reader])
        except Exception as e:
            print(f"Error reading CSV file 'users.csv' with error {e}")

        user_data = []
        for row in user_rows:
            row["userId"] = int(row["userId"])
            user_data.append({key: value for key, value in row.items() if value != ""})

        conn.execute(insert(Users), user_data)

        conn.commit()


def add_data_check():
    with db.engine.connect() as conn:
        result = conn.execute(select(Initialised)).first()

    if result is None:
        add_data()
        with db.engine.connect() as conn:
            conn.execute(insert(Initialised))
            conn.commit()

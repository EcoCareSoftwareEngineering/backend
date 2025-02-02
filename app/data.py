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
        conn.execute(delete(Automations))
        conn.execute(text("ALTER TABLE automations AUTO_INCREMENT = 0;"))
        conn.execute(delete(IotDevices))
        conn.execute(text("ALTER TABLE iot_devices AUTO_INCREMENT = 0;"))
        conn.execute(delete(Tags))
        conn.execute(text("ALTER TABLE tags AUTO_INCREMENT = 0;"))
        conn.execute(delete(IotDeviceUsage))
        conn.execute(text("ALTER TABLE iot_device_usage AUTO_INCREMENT = 0;"))
        conn.execute(delete(EnergySavingGoals))
        conn.execute(text("ALTER TABLE energy_saving_goals AUTO_INCREMENT = 0;"))
        conn.execute(delete(EnergyRecords))
        conn.execute(text("ALTER TABLE energy_records AUTO_INCREMENT = 0;"))
        conn.execute(delete(Users))
        conn.execute(text("ALTER TABLE users AUTO_INCREMENT = 0;"))

        # TODO Finish deleting data
        # TODO Reset autoincrement values to 0

        conn.commit()


def add_data():
    with db.engine.connect() as conn:

        device_rows = []
        with open("data/iot_devices.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            device_rows.extend([row for row in reader])

        device_data = []
        for row in device_rows:
            row["deviceId"] = int(row["deviceId"])
            row["state"] = json.loads(row["state"])
            for entry in row["state"]:
                if entry["datatype"] == "integer":
                    entry["value"] = int(entry["value"])
            row["unlocked"] = bool(row["unlocked"])

            device_data.append({key: value for key, value in row.items() if value != ""})

        # TODO Add data to rest of tables

        conn.execute(insert(IotDevices), device_data)
        
        # Data for tags
        tag_rows = []
        try:
            with open("data/tags.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                tag_rows.extend([row for row in reader])
        except Exception as e:
            print(f"Error reading CSV file: {e}") 
            
        tag_data = []
        
        for row in tag_rows:
            try:
                row["tagId"] = int(row["tagId"])
                row["tagType"] = TagType[row["tagType"]].name # Might need to change from String to Enum here
            
                tag_data.append({key: value for key, value in row.items() if value !=""})
            except Exception as e:
                print(f"Error processing tag row: {row}, Error: {e}")
                continue
            
        if tag_data:
            conn.execute(insert(Tags), tag_data)
            
        # Data for IotDevicesTags (device and tag)
        device_tag_rows = []
        try:
            with open("data/iot_devices_tags.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                device_tag_rows.extend([row for row in reader])
        except Exception as e:
            print(f"Error reading CSV file: {e}")   
        
        device_tag_data = []
        
        for row in device_tag_rows:
            try:
                row["deviceId"] = int(row["deviceId"])
                row["tagId"] = int(row["tagId"])
                device_tag_data.append({key: value for key, value in row.items() if value !=""})
            except Exception as e:
                print(f"Error processing device_tag row: {row}, Error: {e}") 
                continue
            
        if device_tag_data:
            conn.execute(insert(IotDevicesTags), device_tag_data)                 
        
        # Data for IotDeviceUsage 
        device_usage_rows =[]
        try:
            with open("data/iot_device_usage.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                device_usage_rows.extend([row for row in reader])
        except Exception as e:
            print(f"Error reading CSV file: {e}")
        
        device_usage_data = []
        
        for row in device_usage_rows:
            try:
                row["deviceUsageId"] = int(row["deviceUsageId"])
                row["date"] = row["date"] # Date format yyyy-mm-dd
                row["hour"] = int(row["hour"])
                row["usage"] = int(row["usage"])
                row["deviceId"] = int(row["deviceId"]) if row["deviceId"] else None
                device_usage_data.append({key: value for key, value in row.items() if value !=""})
                
            except Exception as e:
                print(f"Error processing IotDeviceUsage row {row}, Error: {e} ")
        
        if device_usage_data:
            try:
                conn.execute(insert(IotDeviceUsage), device_usage_data)
            except Exception as e:
                print(f"Error inserting IotDeviceUsage data in the db: {e}")
        
        # Data for Automations
        automation_rows = []
        try:
            with open("data/automations.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                automation_rows.extend([row for row in reader])
        except Exception as e:
            print(f"Error reading CSV file for Automations: {e}")
            
        automation_data = []
        for row in automation_rows:
            try:
                row["automationId"] = int(row["automationId"])
                row["deviceId"] = int(row["deviceId"])
                row["dateTime"] = row["dateTime"]
                row["newState"] = json.loads(row["newState"])
                automation_data.append({key: value for key, value in row.items() if value !=""})
            except Exception as e:
                print(f"Error processing Automation row: {row},  Errror: {e}")    
        
        if automation_data:
            try:
                conn.execute(insert(Automations), automation_data)
            except Exception as e:
                print(f"Error inserting Automations data in the ds: {e}")
        
        # Data for EnergySavingGoals
        energy_saving_goal_rows = []
        try:
            with open("data/energy_saving_goals.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                energy_saving_goal_rows.extend([row for row in reader])
        except Exception as e:
            print(f"Error reading CSV file for EnergySavingGoals : {e}")
        
        energy_saving_goal_data = []
        for row in energy_saving_goal_rows:
            try:
                row["goalId"] = int(row["goalId"])
                row["name"] = row["name"]
                row["target"] = float(row["goalId"])
                row["progress"] = float(row["progress"])
                row["complete"] = bool(row["complete"])
                row["date"] = row["date"]
                energy_saving_goal_data.append({key: value for key, value in row.items() if value !=""})
            except Exception as e:
                print(f"Error processing EnergySavingGoals row: {row}, Error: {e}")
        if energy_saving_goal_data:
            try:
                conn.execute(insert(EnergySavingGoals), energy_saving_goal_data)
            except Exception as e:
                print(f"Error inserting EnergySavingGoals data in the db: {e}")
                
        # Data for EnergyRecotds
        energy_record_rows = []
        try:
            with open("data/energy_records.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                energy_record_rows.extend([row for row in reader])
        except Exception as e:
            print(f"Error reading CSV file for EnergyRecords : {e}")
        
        energy_record_data = []
        for row in energy_record_rows:
            try:
                row["energyRecordId"] = int(row["energyRecordId"])
                row["date"] = row["date"]
                row["hour"] = int(row["hour"])
                row["energyUse"] = float(row["energyUse"])
                row["energyGeneration"] = float(row["energyGeneration"])
                energy_record_data.append({key: value for key, value in row.items() if value !=""})
            except Exception as e:
                print(f"Error processing EnergyRecords row: {row}, Error: {e}")
        if energy_record_data:
            try:
                conn.execute(insert(EnergyRecords), energy_record_data)
            except Exception as e:
                print(f"Error inserting EnergyRecords data in the db: {e}")
                
        # Data for Users
        user_rows = []
        try:
            with open("data/users.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                user_rows.extend([row for row in reader])
        except Exception as e:
            print(f"Error reading CSV file for Users: {e}")
        
        user_data = []
        for row in user_rows:
            try:
                row["userId"] = int(row["userId"])
                row["name"] = row["name"]
                row["passwordHash"] = row["passwordHash"]
                energy_record_data.append({key: value for key, value in row.items() if value !=""})
            except Exception as e:
                print(f"Error processing Users row: {row}, Error: {e}")
        if user_data:
            try:
                conn.execute(insert(Users), user_data)
            except Exception as e:
                print(f"Error inserting Users data in the db: {e}")             
                
        conn.commit()


def add_data_check():
    with db.engine.connect() as conn:
        result = conn.execute(select(Initialised)).first()

    if result is None:
        add_data()
        with db.engine.connect() as conn:
            conn.execute(insert(Initialised))
            conn.commit()

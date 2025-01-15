from sqlalchemy import select
from . import db
from enum import Enum, auto


class IotState(Enum):
    Ok = auto()
    Fault = auto()


class RecurrenceRate(Enum):
    Hourly = auto()
    Daily = auto()
    Weekly = auto()
    Fortnightly = auto()
    Monthly = auto()


class IotDevicesUserTags(db.Model):
    deviceId = db.Column(
        db.Integer(), db.ForeignKey("iot_devices.deviceId"), primary_key=True
    )
    tagId = db.Column(db.Integer(), db.ForeignKey("tags.tagId"), primary_key=True)


class IotDevicesCustomTags(db.Model):
    deviceId = db.Column(
        db.Integer(), db.ForeignKey("iot_devices.deviceId"), primary_key=True
    )
    tagId = db.Column(db.Integer(), db.ForeignKey("tags.tagId"), primary_key=True)


class DailyRemindersTags(db.Model):
    reminderId = db.Column(
        db.Integer(), db.ForeignKey("daily_reminders.reminderId"), primary_key=True
    )
    tagId = db.Column(db.Integer(), db.ForeignKey("tags.tagId"), primary_key=True)


class Tags(db.Model):
    tagId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    reminders = db.relationship(
        "DailyReminders", secondary=DailyRemindersTags, back_populates="tags"
    )
    iotDeviceUserTags = db.relationship(
        "IotDevices", secondary=IotDevicesUserTags, back_populates="userTags"
    )
    iotDeviceCustomTags = db.relationship(
        "IotDevices", secondary=IotDevicesCustomTags, back_populates="customTags"
    )


class IotDevices(db.Model):
    deviceId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    state = db.Column(db.JSON(), nullable=False)
    status = db.Column(db.Enum(IotState), nullable=False)
    pinCode = db.Column(db.String(4), nullable=True)
    unlocked = db.Column(db.Boolean(), nullable=True)
    uptimeTimestamp = db.Column(db.DateTime(), nullable=True)
    logPath = db.Column(db.String(200), nullable=True, unique=True)
    ipAddress = db.Column(db.String(50), nullable=True, unique=True)
    roomTag = db.Column(db.Integer(), db.ForeignKey("tags.tagId"), nullable=True)
    userTags = db.relationship(
        "Tags", secondary=IotDevicesUserTags, back_populates="iotDeviceUserTags"
    )
    customTags = db.relationship(
        "Tags", secondary=IotDevicesCustomTags, back_populates="iotDeviceCustomTags"
    )
    automations = db.relationship("Automations", back_populates="devices")


class DailyReminders(db.Model):
    reminderId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.Text(), unique=True, nullable=True)
    timeStamp = db.Column(db.DateTime(), nullable=True)
    recurrenceRate = db.Column(db.Enum(RecurrenceRate), nullable=True)
    tags = db.relationship(
        "Tags", secondary=DailyRemindersTags, back_populates="reminders"
    )


class EnergySavingGoals(db.Model):
    goalId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=True)
    target = db.Column(db.Integer(), nullable=False)
    progress = db.Column(db.Integer(), nullable=False, default=0)
    complete = db.Column(db.Boolean(), nullable=False, default=False)
    date = db.Column(db.Date(), nullable=False, default=False)


class EnergyRecords(db.Model):
    energyRecordId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime(), nullable=False)
    energyUse = db.Column(db.Integer(), nullable=False)
    energyGeneration = db.Column(db.Integer(), nullable=False)


class Automations(db.Model):
    automationId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    deviceId = db.Column(
        db.Integer(), db.ForeignKey("iot_devices.deviceId"), nullable=False
    )
    dateTime = db.Column(db.DateTime(), nullable=False)
    newState = db.Column(db.JSON(), nullable=False)
    devices = db.relationship("IotDevices", back_populates="automations")

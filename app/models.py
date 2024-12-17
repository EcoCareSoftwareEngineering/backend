from . import db
from enum import Enum


class IotState(Enum):
    Operating = 0
    Fault = 1


class IotDevice(db.Model):
    deviceId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text(), nullable=True)
    state = db.Column(db.JSON(), nullable=False)
    status = db.Column(db.Enum(IotState), nullable=False)
    pinCode = db.Column(db.String(4), nullable=True)
    uptimeTimestamp = db.Column(db.DateTime(), nullable=True)
    logPath = db.Colum(db.String(200), nullable=True, unique=True)
    ipAddress = db.Colum(db.String(50), nullable=True, unique=True)


class Tag(db.Model):
    pass


class DailyReminder(db.Model):
    pass


class EnergySavingGoals(db.Model):
    goalId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    target = db.Column(db.Integer(), nullable=False)
    progress = db.Column(db.Integer(), nullable=False, default=0)
    complete = db.Column(db.Boolean(), nullable=False, default=False)


class EnergyRecords(db.Model):
    energyRecordId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime(), nullable=False)
    energyUse = db.Column(db.Integer(), nullable=False)
    energyGeneration = db.Column(db.Integer(), nullable=False)

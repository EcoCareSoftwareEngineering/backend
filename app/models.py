from . import db
from enum import Enum, auto


class IotDeviceFaultStatus(Enum):
    Ok = auto()
    Fault = auto()


class IotDeviceStatus(Enum):
    On = auto()
    Off = auto()


class RecurrenceRate(Enum):
    Hourly = auto()
    Daily = auto()
    Weekly = auto()
    Fortnightly = auto()
    Monthly = auto()


class TagType(Enum):
    Room = auto()
    User = auto()
    Custom = auto()


class Initialised(db.Model):
    """
    Internal use only - used as a flag to initialise the DB with data if the DB was just created
    """

    pk = db.Column(db.Integer(), primary_key=True, autoincrement=True)


class IotDevicesTags(db.Model):
    """
    Bridge table between IotDevices and Tags
    deviceId: Foriegn key referencing IotDevices.deviceId
    tagId: Foriegn key referencing Tags.tagId
    """

    deviceId = db.Column(
        db.Integer(), db.ForeignKey("iot_devices.deviceId"), primary_key=True
    )
    tagId = db.Column(db.Integer(), db.ForeignKey("tags.tagId"), primary_key=True)


class Tags(db.Model):
    """
    Stores Tags related to IotDevices
    tagId: Autoincrement primary key
    name: Name of the tag
    tagType: Enum value (see TagType)
    """

    tagId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    tagType = db.Column(db.Enum(TagType), nullable=False)


class IotDevices(db.Model):
    """
    Stores details relating to IoT Devices
    deviceId: Autoincrement primary key
    name: Name of the IoT device
    description: Textual description of the IoT Device
    state: JSON array of IoT Device fields in format
        [
            {
                "fieldName": "name of the field"
                "datatype": "integer" | "float" | "string" | "boolean"
                "value": 0 | 1.2 | "some value" | true // Value matching datatype, these are examples
            }
            ...
        ]
    status: Enum value (IotDeviceStatus), whether the IoT device is On or Off
    faultStatus: Enum value (IoTDeviceFaultStatus), whether the IoT device is Ok or has a Fault
    pinCode: PIN code, if set, 4 digit
    unlocked: Whether the IoT device is unlocked, true if there is no PIN set or if the /devices/unlock/ received the correct PIN
    uptimeTimestamp: Timestamp of when the IoT device turned on
    ipAddress: Private IP address of the IoT device
    """

    deviceId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    state = db.Column(db.JSON(), nullable=False)
    status = db.Column(db.Enum(IotDeviceStatus), nullable=False)
    faultStatus = db.Column(db.Enum(IotDeviceFaultStatus), nullable=False)
    pinCode = db.Column(db.String(4), nullable=True)
    unlocked = db.Column(db.Boolean(), nullable=True)
    uptimeTimestamp = db.Column(db.DateTime(), nullable=True)
    ipAddress = db.Column(db.String(50), nullable=True, unique=True)


class IotDeviceUsage(db.Model):
    """
    Store usage amount for IoT Devices
    deviceUsageId: Autoincrement primary key
    date: Date of usage format - "yyyy-mm-dd"
    hour: Hour number of the day (0-23, 0: 00:00-01:00, 1: 01:00-02:00, ...)
    usage: Minutes active (0-60)
    """

    deviceUsageId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    date = db.Column(db.Date(), nullable=False)
    hour = db.Column(db.Integer(), nullable=False)
    usage = db.Column(db.Integer(), nullable=False)
    deviceId = db.Column(
        db.Integer(), db.ForeignKey("iot_devices.deviceId"), nullable=True
    )


class Automations(db.Model):
    """
    Stores a IoT Device Automation
    automationId: Autoincrement primary key
    deviceId: Foreignn key to IoT Device associated with the automation
    dateTime: Date and Time to run the automation - format "yyyy-mm-dd hh-mm-ss"
    newState: JSON state to update the IoT device with (see IotDevices.state for more info)
    """

    automationId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    deviceId = db.Column(
        db.Integer(), db.ForeignKey("iot_devices.deviceId"), nullable=False
    )
    dateTime = db.Column(db.DateTime(), nullable=False)
    newState = db.Column(db.JSON(), nullable=False)


class EnergySavingGoals(db.Model):
    """
    Stores an Energy Saving Goal
    goalId: Autoincrement primary key
    name: Name of goal
    target: Target amount of energy to save (in kWh)
    progress: Current amount of energy saved (in kWh)
    complete: Whether the goal has been reached
    date: Optional Target Date format - "yyyy-mm-dd"
    """

    goalId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=True)
    target = db.Column(db.Float(), nullable=False)
    progress = db.Column(db.Float(), nullable=False, default=0)
    complete = db.Column(db.Boolean(), nullable=False, default=False)
    date = db.Column(db.Date(), nullable=True)


class EnergyRecords(db.Model):
    """
    Stores Energy Records
    energyRecordId: Autoincrement primary key
    date: Date of record format - "yyyy-mm-dd"
    hour: Hour number of the day (0-23, 0: 00:00-01:00, 1: 01:00-02:00, ...)
    energyUse: Amount of energy used in last hour (in kWh)
    energyGeneration: Amount of energy generated in last hour (in kWh)
    """

    energyRecordId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    date = db.Column(db.Date(), nullable=False)
    hour = db.Column(db.Integer(), nullable=False)
    energyUse = db.Column(db.Float(), nullable=False)
    energyGeneration = db.Column(db.Float(), nullable=False)


class Users(db.Model):
    """
    Stores Users Login Details for local network remote access
    userId: Autoincrement primary key
    passwordHash: Hashed password
    """

    userId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    passwordHash = db.Column(db.String(100), nullable=False)
    salt = db.Column(db.String(100), nullable=False)

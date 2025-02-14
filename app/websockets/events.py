from flask_socketio import SocketIO, emit
from sqlalchemy import select, update

from ..models import IotDeviceFaultStatus, IotDeviceStatus, IotDevices

from .. import db, unconnected_iot_devices


def register_socketio_handlers(socketio: SocketIO):
    @socketio.on("connect")
    def connect_handler():
        with db.engine.connect() as conn:
            statement = select(IotDevices)
            devices = conn.execute(statement)

        connected_iot_devices = []
        for device in devices:
            (
                _,
                name,
                description,
                state,
                status,
                faultStatus,
                _,
                _,
                _,
                ipAddress,
            ) = device

            connected_iot_devices.append(
                {
                    "ipAddress": ipAddress,
                    "name": name,
                    "description": description,
                    "state": state,
                    "status": "On" if status == IotDeviceStatus.On else "Off",
                    "faultStatus": (
                        "Ok" if faultStatus == IotDeviceFaultStatus.Ok else "Fault"
                    ),
                }
            )

        emit("connected_iot_devices", connected_iot_devices)

    @socketio.on("unconnected_iot_devices")
    def receive_unconnected_iot_devices_hander(devices):
        unconnected_iot_devices.clear()
        unconnected_iot_devices.extend(devices)

    @socketio.on("spoof_app_iot_device_update")
    def receive_iot_device_update(device):
        device["status"] = IotDeviceStatus[device["status"]]
        device["faultStatus"] = IotDeviceFaultStatus[device["faultStatus"]]
        statement = (
            update(IotDevices)
            .values(
                state=device["state"],
                status=device["status"],
                faultStatus=device["faultStatus"],
            )
            .where(IotDevices.ipAddress == device["ipAddress"])
        )

        with db.engine.connect() as conn:
            conn.execute(statement)
            conn.commit()


def send_iot_device_update(device_id):
    statement = select(IotDevices).where(IotDevices.deviceId == device_id)
    with db.engine.connect() as conn:
        device = conn.execute(statement).first()

    if device is None:
        return

    (
        _,
        name,
        description,
        state,
        status,
        faultStatus,
        _,
        _,
        _,
        ipAddress,
    ) = device

    device_update = {
        "ipAddress": ipAddress,
        "name": name,
        "description": description,
        "state": state,
        "status": "On" if status == IotDeviceStatus.On else "Off",
        "faultStatus": ("Ok" if faultStatus == IotDeviceFaultStatus.Ok else "Fault"),
    }

    emit("server_iot_device_update", device_update)

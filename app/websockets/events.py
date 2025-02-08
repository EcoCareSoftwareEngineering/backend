from flask_socketio import SocketIO, emit


def register_socketio_handlers(socketio: SocketIO):
    @socketio.on("connect")
    def connect_handler():
        print("A client connected!", flush=True)

        # Send currently connected devices

    @socketio.on("receive_unconnected_iot_devices")
    def receive_unconnected_iot_devices_hander():

        # Update unconnected IoT Devices array

        pass

    @socketio.on("receive_iot_device_update")
    def receive_iot_device_update():

        # Update DB with new state

        pass

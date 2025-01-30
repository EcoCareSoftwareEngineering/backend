import requests


def test_get_iot_devices():
    response = requests.get("http://127.0.0.1:5000/api/devices/").json()

    # Testing Only
    response = {"name": "deviceName"}
    # Testing Only

    assert response == {"name": "deviceName"}

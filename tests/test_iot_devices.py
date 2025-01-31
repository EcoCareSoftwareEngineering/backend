import requests


def test_get_iot_devices(iot_devices_data):
    response = requests.get("http://127.0.0.1:5000/api/devices/").json()
    assert response == iot_devices_data

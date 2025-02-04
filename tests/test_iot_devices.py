import requests


def test_get_iot_devices(
    iot_devices_data,
    automations_data,
    energy_records_data,
    energy_saving_goals_data,
    iot_device_usage_data,
    tags_data,
    users,
):
    response = requests.get("http://127.0.0.1:5000/api/devices/").json()
    assert response == iot_devices_data

import requests

url = "http://127.0.0.1:5000/api/automations/"


def test_get_automations(automations_data):
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == automations_data


def test_post_automations(automations_data):
    newAutomation = {
        "deviceId": 3,
        "dateTime": "2025-02-10 23:20:30",
        "newState": [{"fieldName": "hue", "dataType": "integer", "value": 2}],
    }
    postResponse = requests.post(url, json=newAutomation)
    # now that we've put our new automation in, let's GET the automations
    response = requests.get(url)
    assert postResponse.status_code == 200
    postData = automations_data.copy()
    postData.append(  # create the new output of our get function
        {
            "automationId": 3,
            "deviceId": 3,
            "dateTime": "Mon, 10 Feb 2025 23:20:30 GMT",
            "newState": [{"fieldName": "hue", "dataType": "integer", "value": 2}],
        }
    )
    assert response.json() == postData


def test_put_automations(automations_data):
    putURL = url + "2/"
    updateAutomation = {
        "dateTime": "2025-02-17 22:20:50",
        "newState": [{"fieldName": "huey", "dataType": "integer", "value": 7}],
    }
    # we update the second entry
    putResponse = requests.put(putURL, json=updateAutomation)
    response = requests.get(url)
    assert putResponse.status_code == 200
    putData = automations_data.copy()
    putData[1] = {  # make new compare data
        "automationId": 2,
        "deviceId": 2,
        "dateTime": "Mon, 17 Feb 2025 22:20:50 GMT",
        "newState": [{"fieldName": "huey", "dataType": "integer", "value": 7}],
    }
    assert response.json() == putData


def test_delete_automations(automations_data):
    deleteURL = url + "1/"  # gives automationsId of 1 to delete
    deleteResponse = requests.delete(deleteURL)
    response = requests.get(url)
    assert deleteResponse.status_code == 200
    assert response.json() == [
        automations_data[1]
    ]  # we should only have the second entry left

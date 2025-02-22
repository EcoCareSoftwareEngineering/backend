import requests

# Base URL for energy goals
url = "http://127.0.0.1:5000/api/goals/"


# Test GET request to retrieve all goals
def test_get_goals(login, energy_saving_goals_data):
    response = requests.get(f"{url}", headers={"token": login})

    energy_saving_goals_data[0]["date"] = "Wed, 02 Apr 2025 00:00:00 GMT"
    energy_saving_goals_data[1]["date"] = "Wed, 02 Apr 2025 00:00:00 GMT"
    # Verify status
    assert response.status_code == 200
    assert response.json() == energy_saving_goals_data


def test_post_goals(login, energy_saving_goals_data):
    newGoal = {"name": "Use less heating", "target": 300, "date": "2025-04-17"}
    postResponse = requests.post(url, json=newGoal, headers={"token": login})
    # Get Goal after hopefully creating
    response = requests.get(url, headers={"token": login})
    assert postResponse.status_code == 200
    postData = energy_saving_goals_data.copy()
    postData.append(  # create the new output of our get function
        {
            "goalId": 3,
            "name": "Use less heating",
            "target": 300.0,
            "progress": 0.0,
            "complete": False,
            "date": "Thu, 17 Apr 2025 00:00:00 GMT",
        }
    )
    assert response.json() == postData


def test_put_goal(login, energy_saving_goals_data):
    putURL = url + "2/"
    updateGoal = {
        "name": "Increase Energy Consumption",
        "target": 600,
        "date": "2025-04-17",
    }
    # we update the second entry
    putResponse = requests.put(putURL, json=updateGoal, headers={"token": login})
    response = requests.get(url, headers={"token": login})
    assert putResponse.status_code == 200
    putData = energy_saving_goals_data.copy()
    putData[1] = {  # make new compare data
        "goalId": 2,
        "name": "Increase Energy Consumption",
        "target": 600.0,
        "progress": 200.0,
        "complete": False,
        "date": "Thu, 17 Apr 2025 00:00:00 GMT",
    }
    assert response.json() == putData


def test_delete_goal(login, energy_saving_goals_data):
    deleteURL = url + "1/"  # gives goalId of 1 to delete
    deleteResponse = requests.delete(deleteURL, headers={"token": login})
    response = requests.get(url, headers={"token": login})
    assert deleteResponse.status_code == 200
    assert response.json() == [
        energy_saving_goals_data[1]
    ]  # we should only have the second entry left

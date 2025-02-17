import requests

# Base URL for energy goals
BASE_URL = "http://127.0.0.1:5000/api/goals/"


# Test GET request to retrieve all goals
def test_get_goals(energy_saving_goals_data):
    response = requests.get(f"{BASE_URL}")
    # Verify status
    assert response.status_code == 200
    assert isinstance(response.json(), list)

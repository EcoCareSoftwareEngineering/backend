import pytest
import requests
from datetime import datetime

# Base URL for energy
BASE_URL = "http://127.0.0.1:5000/api/energy/"


# Test GET request to retrive energy records
def test_get_energy_records(login, energy_records_data):
    # GET request to API
    response = requests.get(
        BASE_URL,
        params={"startDate": "2025-01-01", "endDate": "2025-02-01"},
        headers={"token": login},
    )

    assert response.status_code == 200

    data = response.json()

    for record in data:
        record["datetime"] = datetime.strptime(
            record["datetime"], "%a, %d %b %Y %H:%M:%S GMT"
        )

    assert data == energy_records_data


# Test for date range with no records exist
def test_get_energy_records_not_found(login):
    response = requests.get(
        BASE_URL,
        params={"startDate": "2100-01-01", "endDate": "2100-01-02"},
        headers={"token": login},
    )  # Future dates with no data

    # Ensure correct status code
    assert response.status_code == 404

    # Ensure response contains an error message
    data = response.json()
    assert isinstance(data, dict)
    assert "Error" in data
    assert data["Error"] == "No records found for the given date range"

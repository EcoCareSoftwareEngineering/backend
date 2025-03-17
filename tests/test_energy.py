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
        params={"startDate": "2025-01-01", "endDate": "2025-01-09"},
        headers={"token": login},
    )

    assert response.status_code == 200

    data = response.json()

    for record in data:
        record["datetime"] = datetime.strptime(
            record["datetime"], "%Y-%m-%d %H:%M:%S"
        )

    assert data == energy_records_data


# Test for date range with no records exist
def test_get_energy_records_no_results(login):
    response = requests.get(
        BASE_URL,
        params={"startDate": "2100-01-01", "endDate": "2100-01-02"},
        headers={"token": login},
    )  # Future dates with no data

    # Ensure correct status code
    assert response.status_code == 200

    data = response.json()

    # Ensure response contains null/None values
    for record in data:
        assert record['energyUse'] is None
        assert record['energyGeneration'] is None


# Test energy records with time period returns sums
def test_get_energy_records_with_period(login, energy_records_data):
    response = requests.get(
        BASE_URL,
        params={
            "timePeriod": "daily",
            "startDate": "2025-01-01",
            "endDate": "2025-01-09"
            },
        headers={"token": login},
    )  # Future dates with no data

    # Ensure correct status code
    assert response.status_code == 200

    # Format expected data
    expected_data = []
    daily_energy_data = [energy_records_data[i * 24:(i + 1) * 24]
                         for i in range(len(energy_records_data) // 24)]
    for sublist in daily_energy_data:
        day_row = {'energyUse': 0, 'energyGeneration': 0}
        for record in sublist:
            day_row["energyUse"] += record['energyUse']
            day_row["energyGeneration"] += record['energyGeneration']
        expected_data.append(day_row)

    data = response.json()

    # Check length is correct
    assert len(expected_data) == len(data)

    # Ensure response contains summed values
    for expected_values, actual_values in zip(expected_data, data):
        assert round(expected_values['energyUse'], 3) == actual_values['energyUse']
        assert round(expected_values['energyGeneration'], 3) == actual_values['energyGeneration']

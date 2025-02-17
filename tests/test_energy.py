import pytest
import requests

# Base URL for energy
BASE_URL = "http://127.0.0.1:5000/api/energy/"

# Expected energy data for validation for the first record 
expected_record = {
    "energyRecordId": 1,
    "date": "2025-01-01",
    "hour": 0,
    "energyUse": 0.1,
    "energyGeneration": 0
}

# Test GET request to retrive energy records
def test_get_energy_records(energy_records_data):
    # GET request to API
    response = requests.get(BASE_URL, params={"startDate": "2025-01-01", "endDate": "2025-01-02"})
    
    # Verify status
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    # Check for required keys in response
    assert "energyUsage" in data
    assert "energyGeneration" in data
    
    #Validate data in response fields
    assert isinstance(data["energyUsage"], list)
    assert isinstance(data["energyGeneration"], list)
    
    # Make sure the fields are not empty
    assert len(data["energyUsage"]) > 0, "energyUsage list is empty"
    assert len(data["energyGeneration"]) > 0, "energyGeneration list is empty"

    # Get the first record 
    first_record_energy_usage = data["energyUsage"][0]
    first_record_energy_generation = data["energyGeneration"][0]

    # Compare with the expected values
    assert first_record_energy_usage == expected_record["energyUse"], f"Expected {expected_record['energyUse']}, got {first_record_energy_usage}"
    assert first_record_energy_generation == expected_record["energyGeneration"], f"Expected {expected_record['energyGeneration']}, got {first_record_energy_generation}"
    

# Test for date range with no records exist
def test_get_energy_records_not_found():
    response = requests.get(BASE_URL, params={"startDate": "2100-01-01", "endDate": "2100-01-02"})  # Future dates with no data
    
    # Ensure correct status code
    assert response.status_code == 404

    # Ensure response contains an error message
    data = response.json()
    assert isinstance(data, dict)
    assert "Error" in data
    assert data["Error"] == "No records found for the given date range"
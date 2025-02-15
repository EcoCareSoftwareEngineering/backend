import pytest
import requests

# Base URL for energy
BASE_URL = "http://127.0.0.1:5000/api/energy/"

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
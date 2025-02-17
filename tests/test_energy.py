import pytest
import requests

# Base URL for energy
BASE_URL = "http://127.0.0.1:5000/api/energy/"

# Test GET request to retrive energy records
def test_get_energy_records(energy_records_data):
    
    # Filter energy_records_data to match the requested date range (2025-01-01 to 2025-01-02)
    filtered_data = [record for record in energy_records_data if "2025-01-01" <= record["date"] <= "2025-01-02"]
    
    # Arrays energyUse and energyGeneration from filtered energy_records_data
    expected_energy_use_values = [record["energyUse"] for record in filtered_data]
    expected_energy_generation_values = [record["energyGeneration"] for record in filtered_data]
    
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

    # Debugging to see the expected values
    print("Expected Energy Use Values:", expected_energy_use_values)
    print("Expected Energy Generation Values:", expected_energy_generation_values)

    # The Actual data 
    print("Data energyUsage ",  data["energyUsage"])
    print("Data energyGeneration ",  data["energyGeneration"])

    # Compare the energyUSe and energyGeneratin arrays with response
    assert data["energyUsage"] == expected_energy_use_values, f"Expected {expected_energy_use_values}, got {data['energyUsage']}"
    assert data["energyGeneration"] == expected_energy_generation_values, f"Expected {expected_energy_generation_values}, got {data['energyGeneration']}"
    
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
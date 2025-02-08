import pytest
import requests

# Base URL for tags
BASE_URL = "http://127.0.0.1:5000/api/tags/"

@pytest.fixture
def setup_tags():
    # Fixture providing expected tags data
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    return response.json()     

@pytest.fixture
def create_tag():
    # Fixture to create a tag for testing
    new_tag = {"name": "TestTag", "tagType": "Room"}
    response = requests.post(BASE_URL, json=new_tag)
    assert response.status_code == 201
    return response.json()
    

# Test GET request to retrieve all tags
def test_get_tags(setup_tags):
    response = requests.get(BASE_URL)
    # Verify status
    assert response.status_code == 200
    assert response.json() == setup_tags

# Test POST request 
def test_post_tags(setup_tags):
    # Create a new tag
    new_tag ={
        "name": "NewTestTag",
        "tagType": "Room"
    }
    
    response = requests.post(BASE_URL, json=new_tag)
    assert response.status_code == 201
    
    # Check if the tag was created
    created_tag = response.json()
    assert "tagId" in created_tag
    
    # Update expected data
    updated_tags = setup_tags +[{"tagId": created_tag["tagId"], **new_tag}]
    assert requests.get(BASE_URL).json() == updated_tags
   
# Test DELETE request
def test_delete_tags(create_tag):
    # Create a tag 
    tag_id = create_tag["tagId"]
   
    response = requests.delete(f"{BASE_URL}{tag_id}")
    assert response.status_code == 200 # Deleted successfully
    
    # Verify the deleted tag is not available now
    response = requests.get(f"{BASE_URL}{tag_id}")
    assert response.status_code == 404 # Should not be found
    
# Test for single tagId 
def test_get_single_tag(create_tag):
    tag_id = create_tag["tagId"]
        
    response = requests.get(f"{BASE_URL}{tag_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data ==  {"tagId": tag_id, "name": "TestTag", "tagType": "Room"}
    
# Test GET if tagId doesn't exist
def test_get_single_tag_not_found():
    response = requests.get(f"{BASE_URL}9999999") 
    assert response.status_code == 404

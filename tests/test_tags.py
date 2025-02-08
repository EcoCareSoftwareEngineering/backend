import requests

# Base URL for tags
BASE_URL = "http://127.0.0.1:5000/api/tags/"


# Test GET request to retrieve all tags
def test_get_tags():
    response = requests.get(f"{BASE_URL}")
    # Verify status
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test POST request 
def test_post_tags():
    # Create a new tag
    new_tag ={
        "name": "TestTag",
        "tagType": "Room"
    }
    
    response = requests.post(BASE_URL, json=new_tag)
    assert response.status_code == 201
    
    # Check if the tag was created
    data = response.json()
    assert "tagId" in data
    assert data["name"] == new_tag["name"]
    assert data["tagType"] == new_tag["tagType"]
    
    return data["tagId"]

# Test DELETE request
def test_delete_tags():
    # Create a tag 
    tag_id = test_post_tags();
    assert tag_id is not None, "test_post_tags() returned None"
    
    print(f"Deleting tag with ID: {tag_id}")
     
    response = requests.delete(f"{BASE_URL}{tag_id}")
    assert response.status_code == 200 # Deleted successfully
    
    # Verify the deleted tag is not available now
    response = requests.get(f"{BASE_URL}{tag_id}")
    assert response.status_code == 404 # Should not be found
    
    
    
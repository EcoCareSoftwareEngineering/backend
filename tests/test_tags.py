import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/api/tags/"


@pytest.fixture(scope="function")
def create_tag():
    new_tag = {"name": "TestTag", "tagType": "Room"}
    response = requests.post(BASE_URL, json=new_tag)
    assert response.status_code == 201
    return response.json()


def test_get_tags(tags_data):
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert response.json() == tags_data


def test_post_tags(tags_data):
    new_tag = {"name": "NewTestTag", "tagType": "Room"}
    response = requests.post(BASE_URL, json=new_tag)
    assert response.status_code == 201
    created_tag = response.json()
    assert "tagId" in created_tag

    # Fetch just created tag
    updated_tags = tags_data + [{"tagId": created_tag["tagId"], **new_tag}]
    assert requests.get(BASE_URL).json() == updated_tags


def test_delete_tags(create_tag):
    tag_id = create_tag["tagId"]
    response = requests.delete(f"{BASE_URL}{tag_id}")
    assert response.status_code == 200
    response = requests.get(f"{BASE_URL}{tag_id}")
    assert response.status_code == 404


def test_get_single_tag(create_tag):
    tag_id = create_tag["tagId"]
    response = requests.get(f"{BASE_URL}{tag_id}")
    assert response.status_code == 200
    assert response.json() == {"tagId": tag_id, "name": "TestTag", "tagType": "Room"}


def test_get_single_tag_not_found():
    response = requests.get(f"{BASE_URL}9999999")
    assert response.status_code == 404

import requests

url = "http://127.0.0.1:5000/api/unlock/"


def test_get_misc():
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data["pinEnabled"] == True
    assert data["locked"] == True


def test_post_misc():
    pin = {"pinCode": "0000"}
    postresponse = requests.post(url, json=pin)
    response = requests.get(url)
    assert postresponse.status_code == 200
    data = response.json()
    assert response.status_code == 200
    assert data["locked"] == False

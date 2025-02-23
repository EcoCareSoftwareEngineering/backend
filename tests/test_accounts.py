import requests


def test_accounts():
    response = requests.post(
        "http://127.0.0.1:5000/api/accounts/login/",
        json={"username": "newtester", "password": "newtesterpass"},
    )
    assert response.status_code == 500

    response = requests.post(
        "http://127.0.0.1:5000/api/accounts/signup/",
        json={"username": "newtester", "password": "newtesterpass"},
    )
    assert response.status_code == 200

    response = requests.post(
        "http://127.0.0.1:5000/api/accounts/login/",
        json={"username": "newtester", "password": "newtesterpass"},
    )
    assert response.status_code == 200
    assert "token" in response.json()

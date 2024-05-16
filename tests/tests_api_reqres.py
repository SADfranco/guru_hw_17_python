import requests
from jsonschema import validate
from schemas.get_single_user import get_single_user
from schemas.create_user import create_user
from schemas.update_user import update_user

url = 'https://reqres.in'


def test_get_single_user():
    endpoint = '/api/users/'
    id = 2

    response = requests.get(url + endpoint + str(id))
    body = response.json()

    assert response.status_code == 200
    validate(body, get_single_user)
    assert body['data']['id'] == id
    assert body['data']['first_name'] == 'Janet'


def test_create_user():
    endpoint = '/api/users'

    payload = {
        "name": "test_name",
        "job": "test_job"
    }

    response = requests.post(url + endpoint, data=payload)
    body = response.json()

    assert response.status_code == 201
    validate(body, create_user)
    assert body['name'] == 'test_name'
    assert body['job'] == 'test_job'


def test_update_user():
    endpoint = '/api/users/'
    id = 2

    payload = {
        "name": "morpheus",
        "job": "zion resident"
    }

    response = requests.put(url + endpoint + str(id), data=payload)
    body = response.json()

    assert response.status_code == 200
    validate(body, update_user)
    assert body["name"] == "morpheus"
    assert body["job"] == "zion resident"


def test_delete_user():
    endpoint = '/api/users/'
    id = 2
    payload = ""
    headers = {}

    response = requests.delete(url + endpoint + str(id), headers=headers, data=payload)

    assert response.status_code == 204


def test_single_user_not_found():
    endpoint = '/api/users/'
    id = 23

    response = requests.get(url + endpoint + str(id))

    assert response.status_code == 404
    assert response.json() == {}


def test_unsuccessful_register():
    endpoint = '/api/register'

    response = requests.post(url + endpoint)

    assert response.status_code == 400

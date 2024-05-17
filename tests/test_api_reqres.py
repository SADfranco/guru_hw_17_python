import requests
from jsonschema import validate
from schemas.get_single_user import get_single_user
from schemas.create_user import create_user
from schemas.update_user import update_user
from schemas.get_list_users import get_list_users
from schemas.successful_register import successful_register

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


def test_get_list_users():
    endpoint = '/api/users'
    params = {
        "page": 2
    }

    response = requests.get(url + endpoint, params=params)
    body = response.json()
    count_users = [element["id"] for element in body["data"]]

    assert response.status_code == 200
    validate(body, get_list_users)
    assert len(count_users) == len(set(count_users))
    assert body['page'] == params['page']
    assert body['per_page'] == 6


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


def test_successful_register():
    endpoint = '/api/register'

    payload = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }

    response = requests.post(url + endpoint, json=payload)
    body = response.json()

    assert response.status_code == 200
    validate(body, successful_register)
    assert len(body['token']) == 17


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


def test_patch_user():
    endpoint = '/api/users/'
    id = 2

    payload = {
        "name": "morpheus",
        "job": "zion resident"
    }

    response = requests.patch(url + endpoint + str(id), data=payload)
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

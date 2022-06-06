import pytest
from starlette.testclient import TestClient

from minumtium_fastapi import get_minumtium_fastapi
from minumtium_fastapi.deps import DependencyContainer


def test_list_users_is_authenticated(client):
    response = client.get("/users/")
    assert response.status_code == 400


def test_put_users_is_authenticated(client):
    response = client.put("/users/", json={
        'username': 'valid',
        'password': 'valid'
    })
    assert response.status_code == 400


def test_delete_users_is_authenticated(client):
    response = client.delete("/users/valid")
    assert response.status_code == 400


def test_list_users(client):
    response = client.get("/users/", headers={'X-AUTH-MINUMTIUM': 'valid'})
    assert response.status_code == 200

    assert 'users' in response.json()
    assert response.json()['users'] == ['valid', 'another_valid']


def test_put_user(client):
    response = client.put("/users/",
                          json={'username': 'test',
                                'password': 'TwelveChar1!'},
                          headers={'X-AUTH-MINUMTIUM': 'valid'})
    assert response.status_code == 201

    response = response.json()
    assert response['username'] == 'test'
    assert not response['updated']


def test_put_user_update(client):
    response = client.put("/users/",
                          json={'username': 'valid',
                                'password': 'TwelveChar1!'},
                          headers={'X-AUTH-MINUMTIUM': 'valid'})
    assert response.status_code == 201

    response = response.json()
    assert response['username'] == 'valid'
    assert response['updated']


def test_put_user_empty(client):
    response = client.put("/users/",
                          json={'username': '',
                                'password': 'TwelveChar1!'},
                          headers={'X-AUTH-MINUMTIUM': 'valid'})
    assert response.status_code == 400
    assert response.json()['detail'] == 'Empty usernames are not accepted.'


def test_put_user_invalid_password(client):
    response = client.put("/users/",
                          json={'username': 'valid',
                                'password': 'invalid'},
                          headers={'X-AUTH-MINUMTIUM': 'valid'})
    assert response.status_code == 400


def test_delete_user(client):
    response = client.delete("/users/valid", headers={'X-AUTH-MINUMTIUM': 'valid'})
    assert response.status_code == 200
    assert response.json()['username'] == 'valid'


def test_delete_user_invalid(client):
    response = client.delete("/users/invalid", headers={'X-AUTH-MINUMTIUM': 'valid'})
    assert response.status_code == 400
    assert response.json()['detail'] == 'User does not exist: invalid'


def test_delete_user_empty(client):
    response = client.delete("/users/", headers={'X-AUTH-MINUMTIUM': 'valid'})
    assert response.status_code == 405


@pytest.fixture()
def client(users_database_adapter, mock_authentication) -> TestClient:
    di_context = DependencyContainer()
    di_context.database_adapter_users = users_database_adapter
    di_context.authenticate = mock_authentication

    minumtium = get_minumtium_fastapi(di_context=di_context)
    client = TestClient(minumtium)
    return client

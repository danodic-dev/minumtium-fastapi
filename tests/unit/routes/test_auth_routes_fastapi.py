import pytest
from minumtium.modules.idm import MAX_LOGIN_TRIALS
from starlette.testclient import TestClient

import deps
from minumtium_fastapi import get_minumtium_fastapi
from minumtium_fastapi.deps import database_adapter_users


def test_login(client):
    response = client.post("/auth/login", json={
        'username': 'valid',
        'password': 'valid'
    })
    assert response.status_code == 200
    assert response.json() is not None
    assert len(response.json()['token']) > 0


@pytest.mark.parametrize('username, password', [('valid', 'invalid'),
                                                ('invalid', 'valid')])
def test_login_invalid_username_password(client, username, password):
    response = client.post("/auth/login", json={
        'username': username,
        'password': password
    })
    assert response.status_code == 401
    assert response.json() is not None
    assert response.json()['detail'] == 'Invalid username and/or password.'
    assert 'token' not in response.json()


def test_login_max_attempts(client):
    for _ in range(MAX_LOGIN_TRIALS):
        client.post("/auth/login", json={
            'username': 'valid',
            'password': 'invalid'
        })

    response = client.post("/auth/login", json={
        'username': 'valid',
        'password': 'valid'
    })

    assert response.status_code == 401
    assert response.json() is not None
    assert response.json()['detail'] == 'Invalid username and/or password.'
    assert 'token' not in response.json()


@pytest.fixture()
def client(users_database_adapter) -> TestClient:
    async def override_adapter():
        return users_database_adapter

    minumtium = get_minumtium_fastapi()
    client = TestClient(minumtium)
    minumtium.dependency_overrides[database_adapter_users] = override_adapter
    return client

def test_login(clients):
    for client in clients:
        response = client.post('/auth/login', json={
            'username': 'minumtium',
            'password': 'minumtium'
        })
        assert response.status_code == 200
        assert response.json() is not None
        assert len(response.json()['token']) > 0


def test_login_invalid_username_password(clients):
    for client in clients:
        response = client.post('/auth/login', json={
            'username': 'minumtium',
            'password': 'invalid'
        })
        assert response.status_code == 401
        assert response.json() is not None
        assert response.json()['detail'] == 'Invalid username and/or password.'
        assert 'token' not in response.json()

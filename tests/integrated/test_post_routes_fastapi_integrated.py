def test_get_post(clients):
    for client in clients:
        response = client.get('/posts/get/0')
        assert response.status_code == 200
        assert response.json() == {'id': '0',
                                   'title': 'This is the first post',
                                   'author': 'danodic',
                                   'timestamp': '2022-02-22T12:22:22.222222',
                                   'body': 'This is a sample post.'}


def test_get_post_invalid_id(clients):
    for client in clients:
        response = client.get('/posts/get/200')
        assert response.status_code == 404
        assert response.json() == {'detail': 'Post not found: 200'}


def test_get_summary(clients):
    for client in clients:
        response = client.get('/posts/summary')
        assert response.status_code == 200

        assert len(response.json()['posts']) == 5

        post = response.json()['posts'][0]
        assert post == {'id': '0',
                        'title': 'This is the first post',
                        'author': 'danodic',
                        'timestamp': '2022-02-22T12:22:22.222222'}

        post = response.json()['posts'][4]
        assert post == {'id': '4',
                        'title': 'This is the fifth post',
                        'author': 'danodic',
                        'timestamp': '2022-02-22T08:22:22.222222'}


def test_get_posts_for_page(clients):
    for client in clients:
        response = client.get('/posts/page/0')
        assert response.status_code == 200

        assert len(response.json()['posts']) == 5

        post = response.json()['posts'][0]
        assert post == {'id': '0',
                        'title': 'This is the first post',
                        'author': 'danodic',
                        'body': 'This is a sample post.',
                        'timestamp': '2022-02-22T12:22:22.222222'}

        post = response.json()['posts'][4]
        assert post == {'id': '4',
                        'title': 'This is the fifth post',
                        'author': 'danodic',
                        'body': 'This is a sample post.',
                        'timestamp': '2022-02-22T08:22:22.222222'}


def test_get_page_wrong_page(clients):
    for client in clients:
        response = client.get('/posts/page/10')
        assert response.status_code == 200
        assert response.json()['posts'] == []


def test_get_page_invalid_page(clients):
    for client in clients:
        response = client.get('/posts/page/invalid')
        assert response.status_code == 422


def test_add_post(clients):
    for client in clients:
        response = client.post('/auth/login', json={
            'username': 'minumtium',
            'password': 'minumtium'
        })
        assert 'token' in response.json()
        token = response.json()['token']

        response = client.post('/posts/add', json={
            'author': 'Sample Author',
            'title': 'Sample Title',
            'body': 'Sample Body'}, headers={'X-AUTH-MINUMTIUM': token})
        assert response.status_code == 201
        inserted_id = response.json()['id']

        response = client.get(f'/posts/get/{inserted_id}')
        assert response.status_code == 200

        response = response.json()
        assert response['id'] == inserted_id
        assert response['title'] == 'Sample Title'
        assert response['author'] == 'Sample Author'
        assert response['body'] == 'Sample Body'
        assert 'timestamp' in response and isinstance(response['timestamp'], str)

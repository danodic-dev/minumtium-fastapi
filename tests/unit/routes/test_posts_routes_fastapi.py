from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from minumtium.modules.posts import Post

import deps
from minumtium_fastapi import get_minumtium_fastapi
from minumtium_fastapi.auth import authenticate
from minumtium_fastapi.deps import database_adapter_posts


def test_get_post(client):
    response = client.get("/posts/get/0")
    assert response.status_code == 200
    data = Post.parse_obj(response.json())
    assert data.dict() == {'id': '0',
                           'title': 'This is the first post',
                           'author': 'danodic',
                           'timestamp': datetime(2022, 2, 22, 12, 22, 22, 222222),
                           'body': 'This is a sample post.'}


def test_get_latest_post(client):
    response = client.get("/posts/get/latest")
    assert response.status_code == 200
    data = Post.parse_obj(response.json())
    assert data.dict() == {'id': '0',
                           'title': 'This is the first post',
                           'author': 'danodic',
                           'timestamp': datetime(2022, 2, 22, 12, 22, 22, 222222),
                           'body': 'This is a sample post.'}


def test_get_post_invalid_id(client):
    response = client.get("/posts/get/invalid")
    assert response.status_code == 404
    data = response.json()
    assert data == {'detail': 'Post not found: invalid'}


def test_get_summary(client):
    response = client.get("/posts/summary")
    assert response.status_code == 200

    posts = [Post.parse_obj(entry) for entry in response.json()['posts']]
    assert len(posts) == 5

    assert posts[0].id == '0'
    assert posts[4].id == '4'

    post = posts[0]
    assert post.body is None
    assert post.title == 'This is the first post'
    assert post.author == 'danodic'
    assert post.timestamp is not None


def test_get_posts_for_page(client):
    response = client.get("/posts/page/0")
    assert response.status_code == 200

    first_post, second_post, third_post, fourth_post, fifth_post = [Post.parse_obj(entry) for entry in
                                                                    response.json()['posts']]

    assert first_post.id == '0'
    assert first_post.body == 'This is a sample post.'
    assert first_post.title == 'This is the first post'
    assert first_post.author == 'danodic'
    assert first_post.timestamp is not None

    assert fifth_post.id == '4'
    assert fifth_post.body == 'This is a sample post.'
    assert fifth_post.title == 'This is the fifth post'
    assert fifth_post.author == 'danodic'
    assert fifth_post.timestamp is not None


@pytest.mark.parametrize('page', ['invalid', -1])
def test_get_page_invalid_page(page, client):
    response = client.get(f"/posts/page/{page}")
    assert response.status_code == 422


def test_add_post(client):
    response = client.post(f'/posts/add', json={
        'author': 'Sample Author',
        'title': 'Sample Title',
        'body': 'Sample Body'}, headers={'X-AUTH-MINUMTIUM': 'valid'})
    assert response.status_code == 201
    assert response.json() == {'id': '0'}


def test_add_post_is_authenticated(client):
    response = client.post(f'/posts/add', json={
        'author': 'Sample Author',
        'title': 'Sample Title',
        'body': 'Sample Body'}, headers={'X-AUTH-MINUMTIUM': 'invalid'})
    assert response.status_code == 401


@pytest.fixture()
def client(posts_database_adapter, mock_authentication) -> TestClient:
    async def override_adapter():
        return posts_database_adapter

    minumtium = get_minumtium_fastapi()
    client = TestClient(minumtium)
    minumtium.dependency_overrides[database_adapter_posts] = override_adapter
    minumtium.dependency_overrides[authenticate] = mock_authentication
    return client

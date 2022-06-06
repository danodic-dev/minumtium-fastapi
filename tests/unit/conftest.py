from typing import Dict, List

import pytest
from fastapi import Header
from minumtium.infra.authentication import AuthenticationException, AuthenticationService
from minumtium.infra.database import DataNotFoundException
from minumtium.modules.posts import PostNotFoundException

from minumtium_fastapi.auth import NoTokenProvidedException, NotAuthorizedException


@pytest.fixture()
def mock_authentication():
    def wrapper(x_auth_minumtium: str = Header(None)):
        if x_auth_minumtium is None:
            raise NoTokenProvidedException()
        elif x_auth_minumtium != 'valid':
            raise NotAuthorizedException()

    return wrapper


@pytest.fixture
def auth_service():
    class MockAuthenticationAdapter:
        def validate_token(self, token: str) -> bool:
            return token == 'valid'

        def authenticate(self, username: str, password: str) -> str:
            if username == 'valid' and password == 'valid':
                return 'valid'
            raise AuthenticationException()

    # noinspection PyTypeChecker
    return AuthenticationService(MockAuthenticationAdapter())


@pytest.fixture()
def users_database_data() -> List:
    return [{'id': '0',
             'username': 'valid',
             'encrypted_password': '$2b$14$WPJmYmygdinbCJ3V4.N/c.X8llM3aTYlKs5gKFIalKq0rK7B1.R.i'},
            {'id': '1',
             'username': 'another_valid',
             'encrypted_password': '$2b$14$WPJmYmygdinbCJ3V4.N/c.X8llM3aTYlKs5gKFIalKq0rK7B1.R.i'}]


@pytest.fixture()
def users_database_adapter(users_database_data):
    class MockAdapter:
        def __init__(self, data: Dict):
            self.data = data

        def all(self, *args, **kwargs):
            return self.data

        def find_by_criteria(self, criteria: Dict) -> List[Dict]:
            for user in self.data:
                for field, value in criteria.items():
                    if user[field] != value:
                        break
                else:
                    return [user]
            raise DataNotFoundException()

        def insert(self, data: Dict) -> str:
            return '0'

        def delete(self, id: str):
            for user in self.data:
                if user['id'] == id:
                    break
            else:
                raise DataNotFoundException()

    # noinspection PyTypeChecker
    return MockAdapter(users_database_data)


@pytest.fixture()
def posts_database_adapter(posts_database_data: Dict):
    class MockAdapter:
        def __init__(self, data: Dict):
            self.data = data

        def count(self) -> int:
            return len(self.data)

        def find_by_id(self, id: str) -> Dict:
            for post in self.data:
                if post['id'] == id:
                    return post
            else:
                raise PostNotFoundException(id)

        def insert(self, *args, **kwargs) -> str:
            return '0'

        def all(self, limit: int = None, skip: int = None, sort_by=None):
            if limit is None and skip is None:
                return self.data
            if limit is None:
                return self.data[skip:]
            if skip is None:
                return self.data[:limit]
            return self.data[skip:skip + limit]

        def summary(self, projection: List[str], limit: int = None, sort_by=None):
            projected_data = []
            for post in self.data[:limit]:
                entry = {}
                for field in projection:
                    entry[field] = post[field]
                projected_data.append(entry)
            return projected_data

    return MockAdapter(posts_database_data)

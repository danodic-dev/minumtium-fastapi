from typing import Dict, List

import pytest
from fastapi.testclient import TestClient
from minumtium_postgres import MinumtiumPostgresAdapter, MinumtiumPostgresAdapterConfig
from minumtium_sqlite import MinumtiumSQLiteAdapterConfig, MinumtiumSQLiteAdapter

from minumtium_fastapi import get_minumtium_fastapi


@pytest.fixture(scope='function')
def postgres_config() -> MinumtiumPostgresAdapterConfig:
    return MinumtiumPostgresAdapterConfig(username='minumtium',
                                          password='minumtium',
                                          host='127.0.0.1',
                                          port=5432,
                                          dbname='minumtium',
                                          schema_name='public')


@pytest.fixture(scope='function')
def postgres_posts_adapter(postgres_config: MinumtiumPostgresAdapterConfig):
    adapter = MinumtiumPostgresAdapter(postgres_config, table_name='posts')
    adapter.truncate()
    return adapter


@pytest.fixture(scope='function')
def postgres_users_adapter(postgres_config: MinumtiumPostgresAdapterConfig):
    adapter = MinumtiumPostgresAdapter(postgres_config, table_name='users')
    adapter.truncate()
    return adapter


@pytest.fixture(scope='function')
def postgres_client(postgres_posts_adapter: MinumtiumPostgresAdapter,
                    postgres_users_adapter: MinumtiumPostgresAdapter,
                    posts_database_data: List[Dict]):
    postgres_posts_adapter.truncate()
    for post in posts_database_data:
        postgres_posts_adapter.insert(post)

    minumtium = get_minumtium_fastapi(database_adapter_posts=postgres_posts_adapter,
                                      database_adapter_users=postgres_users_adapter)
    return TestClient(minumtium)


@pytest.fixture(scope='function')
def sqlite_config() -> MinumtiumSQLiteAdapterConfig:
    return MinumtiumSQLiteAdapterConfig(schema_name='minumtium')


@pytest.fixture(scope='function')
def sqlite_posts_adapter(sqlite_config: MinumtiumSQLiteAdapterConfig):
    adapter = MinumtiumSQLiteAdapter(sqlite_config, table_name='posts')
    adapter.truncate()
    return adapter


@pytest.fixture(scope='function')
def sqlite_users_adapter(sqlite_config: MinumtiumSQLiteAdapterConfig):
    adapter = MinumtiumSQLiteAdapter(sqlite_config, table_name='users')
    adapter.truncate()
    return adapter


@pytest.fixture(scope='function')
def sqlite_client(sqlite_posts_adapter, sqlite_users_adapter):
    app = get_minumtium_fastapi(database_adapter_posts=sqlite_posts_adapter,
                                database_adapter_users=sqlite_users_adapter)
    return TestClient(app)


@pytest.fixture(scope='function')
def clients(sqlite_client, postgres_client):
    return [sqlite_client, postgres_client]

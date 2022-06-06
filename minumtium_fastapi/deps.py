from minumtium.infra.authentication import AuthenticationAdapter, AuthenticationService
from minumtium.infra.database import DatabaseAdapter
from minumtium.modules.idm import UserRepository, IdmService
from minumtium.modules.posts import PostRepository, PostService

from .auth import setup_authenticate_dependency


class DependencyContainer:

    def __init__(self,
                 database_adapter_posts: DatabaseAdapter = None,
                 database_adapter_users: DatabaseAdapter = None,
                 authentication_adapter: AuthenticationAdapter = None,
                 authentication_function=None):

        self.database_adapter_posts = database_adapter_posts
        if not self.database_adapter_posts:
            self.database_adapter_posts = self.__instantiate_database_adapter('posts')

        self.database_adapter_users = database_adapter_users
        if not self.database_adapter_users:
            self.database_adapter_users = self.__instantiate_database_adapter('users')

        self.authentication_adapter = authentication_adapter
        if not self.authentication_adapter:
            self.authentication_adapter = self.__instantiate_authentication_adapter(self.database_adapter_users)

        self.posts_repository = PostRepository(self.database_adapter_posts)
        self.posts_service = PostService(self.posts_repository)

        self.users_repository = UserRepository(self.database_adapter_users)

        self.auth_service = AuthenticationService(self.authentication_adapter)
        self.idm_service = IdmService(self.authentication_adapter, self.users_repository)

        self.authenticate = authentication_function
        if self.authenticate is None:
            self.authenticate = setup_authenticate_dependency(self.auth_service)

    @staticmethod
    def __instantiate_database_adapter(table_name: str):
        from minumtium_sqlite import MinumtiumSQLiteAdapterConfig, MinumtiumSQLiteAdapter
        config = MinumtiumSQLiteAdapterConfig(schema_name='minumtium')
        return MinumtiumSQLiteAdapter(config, table_name)

    @staticmethod
    def __instantiate_authentication_adapter(users_adapter):
        from minumtium_simple_jwt_auth import MinumtiumSimpleJwtAuthentication, \
            MinumtiumSimpleJwtAuthenticationConfig
        config = MinumtiumSimpleJwtAuthenticationConfig(jwt_key='not a reliable key, change that quickly',
                                                        session_duration_hours=1)
        return MinumtiumSimpleJwtAuthentication(config, users_adapter)

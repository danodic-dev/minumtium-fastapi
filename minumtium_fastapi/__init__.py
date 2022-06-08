from minumtium.infra.authentication import AuthenticationAdapter
from minumtium.infra.database import DatabaseAdapter

from minumtium_fastapi.deps import DependencyContainer
from minumtium_fastapi.routes.auth import get_auth_router
from minumtium_fastapi.routes.posts import get_posts_router
from minumtium_fastapi.routes.users import get_users_router


def get_minumtium_fastapi(database_adapter_posts: DatabaseAdapter = None,
                          database_adapter_users: DatabaseAdapter = None,
                          authentication_adapter: AuthenticationAdapter = None,
                          include_user_endpoints: bool = True,
                          di_context: DependencyContainer = None):
    """
    Creates a FastAPI instance for the minumtium_fastapi application that can either be started as an stand-alone
    application using a wrapper like or can be integrated as a sub-app into a bigger fastapi application.

    :param authentication_adapter: an adapter that implements the AuthenticationAdapter interface.
    :param database_adapter_users: an adapter that implements the DatabaseAdapter interface and is setup to use the
                                   'users' table/collection.
    :param database_adapter_posts: an adapter that implements the DatabaseAdapter interface and is setup to use the
                                   'posts' table/collection.
    :param include_user_endpoints: defines if the user management endpoints should be added to the minumtium_fastapi
                                   application routes. It can be suppressed if you are using a custom authentication
                                   adapter and do not need the minumtium_fastapi user management features.
    :param di_context: injects a custom dependency injection container, useful for testing.
    :return: an instance of FastAPI that can be embedded into another FastAPI app, or run stand-alone using a wrapper
             like uvicorn.
    """
    from fastapi import FastAPI

    context = di_context
    if not di_context:
        context = DependencyContainer(database_adapter_posts,
                                      database_adapter_users,
                                      authentication_adapter)

    minumtium = FastAPI()
    minumtium.include_router(get_posts_router(context))
    minumtium.include_router(get_auth_router(context))

    if include_user_endpoints:
        minumtium.include_router(get_users_router(context))

    return minumtium

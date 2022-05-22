# Minumtium FastAPI

A FastAPI application layer for the [minumtium](https://github.com/danodic-dev/minumtium) library.

### How it works

This library will provide you REST endpoints for authentication, user management and posts. It will use by default the
[Simple JWT Auth Adapter](https://github.com/danodic-dev/minumtium-simple-jwt-auth) for authentication and the
[SQLite Adapter](https://github.com/danodic-dev/minumtium-sqlite) for data access/storage, but you can provide your own
adapters if needed. Also, exposing the user management endpoints is optional, for the cases where you have your
own user management and/or authentication systems and don't want to use the built-in ones.

This library is meant to be integrated into a bigger FastAPI application, so you can extend your application adding very
simple blogging functionality to it.

## Usage

Install it using your favorite package manager:

```commandline
pip install minumtium-fastapi
```

```commandline
pipenv install minumtium-fastapi
```

```commandline
poetry install minumtium-fastapi
```

Then, get the FastAPI router to connect it as a subapp into your main FastAPI app:

```python
from fastapi import FastAPI

import minumtium_fastapi

# Create the minumtium subapp
minumtium = minumtium_fastapi.get_minumtium_fastapi()

# Mount minumtium into your main application, with whatever prefix you would like
main_application = FastAPI()
main_application.mount('/minumtium', main_application)
```

You will get an instance that will use an in-memory sqlite and the standard JWT authentication when you call
`minumtium_fastapi.get_minumtium_fastapi()` without passing any arguments.

### Providing Custom Adapters

You can also provide your own adapters for data and authentication and disable the user management endpoints.

```python
from fastapi import FastAPI

import minumtium_fastapi

from my_cool_app import MyCoolDatabaseAdapter, MyCoolAuthenticationAdapter

# Create your adapters
database_adapter_posts = MyCoolDatabaseAdapter('posts')
database_adapter_users = MyCoolDatabaseAdapter('users')
authentication_adapter = MyCoolAuthenticationAdapter()

# Create the minumtium subapp
minumtium = minumtium_fastapi.get_minumtium_fastapi(database_adapter_posts,
                                                    database_adapter_users,
                                                    include_user_endpoints=False)

# Mount minumtium into your main application, with whatever prefix you would like
main_application = FastAPI()
main_application.mount('/minumtium', main_application)
```

### Running Standalone

You can also run it standalone, but this is probably useless. Create a file named `main.py` with the following contents:

```python
from fastapi import FastAPI

import minumtium_fastapi

app = FastAPI()
app.mount('/minumtium', minumtium_fastapi.get_minumtium_fastapi())
```

Then execute it in the terminal:

```commandline
uvicorn main:app --reload
```

## API Docs

You will be able to see the API docs going to `/<minumtium mount path>/docs` in a running instance of minumtium. 
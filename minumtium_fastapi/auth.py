from fastapi import Header, HTTPException
from minumtium.infra.authentication import AuthenticationService, AuthenticationException


def setup_authenticate_dependency(service: AuthenticationService):
    async def authenticate(x_auth_minumtium: str = Header(None)):
        if x_auth_minumtium is None:
            raise NoTokenProvidedException()
        try:
            service.validate_token(x_auth_minumtium)
        except AuthenticationException as e:
            raise NotAuthorizedException() from e

    return authenticate


class NoTokenProvidedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='Authentication token has not been provided.')


class NotAuthorizedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail='Not authorized.')

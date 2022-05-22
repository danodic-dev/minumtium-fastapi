import pytest

from minumtium_fastapi.auth import authenticate, NoTokenProvidedException, NotAuthorizedException


@pytest.mark.asyncio
async def test_authenticate_valid_token(auth_service):
    await authenticate('valid', auth_service)


@pytest.mark.asyncio
async def test_authenticate_invalid_token(auth_service):
    with pytest.raises(NotAuthorizedException):
        await authenticate('invalid', auth_service)


@pytest.mark.asyncio
async def test_authenticate_no_token(auth_service):
    with pytest.raises(NoTokenProvidedException):
        await authenticate(None, auth_service)

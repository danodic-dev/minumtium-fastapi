import pytest

from minumtium_fastapi.auth import NoTokenProvidedException, NotAuthorizedException, setup_authenticate_dependency


@pytest.mark.asyncio
async def test_authenticate_valid_token(auth_service):
    await setup_authenticate_dependency(auth_service)('valid', auth_service)


@pytest.mark.asyncio
async def test_authenticate_invalid_token(auth_service):
    with pytest.raises(NotAuthorizedException):
        await setup_authenticate_dependency(auth_service)('invalid', auth_service)


@pytest.mark.asyncio
async def test_authenticate_no_token(auth_service):
    with pytest.raises(NoTokenProvidedException):
        await setup_authenticate_dependency(auth_service)(None, auth_service)

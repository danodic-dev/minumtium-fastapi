from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from minumtium.infra.authentication import AuthenticationService, AuthenticationException
from pydantic import BaseModel

from ..deps import DependencyContainer


class AuthRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    token: str


def get_auth_router(context: DependencyContainer) -> APIRouter:
    auth_router = APIRouter(
        prefix='/auth',
        tags=['auth']
    )

    service: AuthenticationService = context.auth_service

    @auth_router.post('/login', response_model=AuthResponse)
    async def login(login_data: AuthRequest):
        try:
            token = service.authenticate(login_data.username, login_data.password)
            return AuthResponse(token=token)
        except AuthenticationException as e:
            raise HTTPException(status_code=401, detail=str(e))

    return auth_router

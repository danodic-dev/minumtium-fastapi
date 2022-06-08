from typing import List

from fastapi import APIRouter, HTTPException, Depends
from minumtium.modules.posts import (PostNotFoundException,
                                     InvalidPageArgumentException,
                                     Post, NoPostsException)
from pydantic import BaseModel

from ..deps import DependencyContainer


class GetPostsResponse(BaseModel):
    posts: List[Post]


class GetPagesResponse(BaseModel):
    page_count: int


class AddPostRequest(BaseModel):
    author: str
    title: str
    body: str


class AddPostResponse(BaseModel):
    id: str


def get_posts_router(context: DependencyContainer) -> APIRouter:
    posts_router = APIRouter(
        prefix='/posts',
        tags=['posts']
    )

    service = context.posts_service
    authenticate = context.authenticate

    @posts_router.get('/get/latest', response_model=Post)
    async def get_latest_post():
        try:
            return service.get_latest_post()
        except NoPostsException as e:
            raise HTTPException(status_code=404, detail=str(e))

    @posts_router.get('/get/{post_id}', response_model=Post)
    async def get_posts(post_id: str):
        try:
            return service.get_post(post_id)
        except PostNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))

    @posts_router.get('/summary', response_model=GetPostsResponse, response_model_exclude_none=True)
    async def get_summary():
        return GetPostsResponse(posts=service.get_latest_posts_summary())

    @posts_router.get('/page/{page}', response_model=GetPostsResponse)
    async def get_posts(page: int):
        try:
            return GetPostsResponse(posts=service.get_posts_for_page(page))
        except InvalidPageArgumentException as e:
            raise HTTPException(status_code=422, detail=str(e))

    @posts_router.get('/pages', response_model=GetPagesResponse)
    async def get_posts():
        return GetPagesResponse(page_count=service.get_page_count())

    @posts_router.post('/add', response_model=AddPostResponse, status_code=201, dependencies=[Depends(authenticate)])
    async def add_post(post: AddPostRequest):
        try:
            post_id = service.add_post(**post.dict())
            return AddPostResponse(id=post_id)
        except InvalidPageArgumentException as e:
            raise HTTPException(status_code=422, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return posts_router

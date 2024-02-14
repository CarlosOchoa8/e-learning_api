from app.endpoints import (
    user_router,
    course_router,
    lesson_router,
    lesson_file_router,
    progress_router,
    websocket_router,
)
from fastapi import APIRouter


api_router = APIRouter()

api_router.include_router(
    router=user_router,
    prefix='/users',
    tags=['users'],
    responses={418: {'description': 'I"m a teapot =)'}}
)

api_router.include_router(
    router=course_router,
    prefix='/courses',
    tags=['courses'],
    responses={418: {'description': 'I"m a teapot =)'}}
)

api_router.include_router(
    router=lesson_router,
    prefix='/lessons',
    tags=['lessons'],
    responses={418: {'description': 'I"m a teapot =)'}}
)

api_router.include_router(
    router=lesson_file_router,
    prefix='/lesson_files',
    tags=['lesson_files'],
    responses={418: {'description': 'I"m a teapot =)'}}
)

api_router.include_router(
    router=progress_router,
    prefix='/progress',
    tags=['progress'],
    responses={418: {'description': 'I"m a teapot =)'}}
)

api_router.include_router(
    router=websocket_router,
    prefix='/websocket',
    tags=['websocket'],
    responses={418: {'description': 'I"m a teapot =)'}}
)

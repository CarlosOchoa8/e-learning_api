from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api.routers import api_router
from app.config.statics import statics

fastapi_app = FastAPI(
    title='e-learning_api',
    description='e-learning platform API',
    # docs_url=None, # Disable docs (Swagger UI)
    # redoc_url=None, # Disable redoc
    swagger_ui_parameters={'docExpansion': 'None'}
)

fastapi_app.include_router(
    router=api_router,
    prefix='/api/v1'
)

fastapi_app.mount(
    '/statics', StaticFiles(directory=statics, html=True), name='statics'
)
app = fastapi_app

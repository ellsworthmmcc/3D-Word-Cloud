from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn

from backend.routers import analyze
from backend.database.database import Base, engine, get_db


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title='3D-Word-Cloud-Ellsworth',
    description='Generates 3D word clouds from links',
    version='0.1.0',
    docs_url='/docs',
    redoc_url='/redoc',
    lifespan=lifespan
)

app.include_router(analyze.router, prefix='/analyze', tags=['analyze'])


@app.get('/', include_in_schema=False, name='home')
async def home(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    return {'test': 'This is a test'}


@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(
    request: Request,
    exception: StarletteHTTPException,
):
    return await http_exception_handler(request, exception)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exception: RequestValidationError,
):
    return await request_validation_exception_handler(request, exception)
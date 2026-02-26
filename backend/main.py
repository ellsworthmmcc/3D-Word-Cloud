from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn

from database import Base, engine, get_db


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


@app.get('/', include_in_schema=False, name='home')
async def home(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    pass


if __name__ == '__main__':
    uvicorn.run("main.app", host="0.0.0.0", port=8000, reload=True)

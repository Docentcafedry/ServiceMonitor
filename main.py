import asyncio
import logging
import aiohttp
from contextlib import asynccontextmanager
from fastapi import FastAPI
from db import engine, Base
from middlewares import RequestLoggingMiddleware
from service import get_status_for_all_domains
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db_connection, async_session

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def wait(db_session: AsyncSession):
    while True:
        await asyncio.sleep(60 * 5)
        async with aiohttp.ClientSession() as session:
            await get_status_for_all_domains(session=session, db_session=db_session)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        print("Successfully created db tables!")
    generator = get_db_connection()
    db_session = await anext(generator)
    asyncio.create_task(wait(db_session=db_session))
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(RequestLoggingMiddleware, logger=logger)


@app.get("/")
async def greeting():
    await asyncio.sleep(2)
    return {"message": "Hello World"}

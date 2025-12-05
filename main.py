import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from db import engine, Base
from middlewares import RequestLoggingMiddleware

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        print("Successfully created db tables!")
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(RequestLoggingMiddleware, logger=logger)


@app.get("/")
async def greeting():
    await asyncio.sleep(2)
    return {"message": "Hello World"}

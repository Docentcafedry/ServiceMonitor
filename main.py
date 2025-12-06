import asyncio
import logging
from http.client import HTTPException

import aiohttp
from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, status, HTTPException
from db import engine, Base
from middlewares import RequestLoggingMiddleware
from service import get_status_for_all_domains
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db_connection, async_session
from depends import db_connection
from service import add_domain, get_domain_with_examinations
from exceptions import DomainAlreadyExistsError, NoDomainFoundError

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def wait(db_session: AsyncSession):
    while True:
        async with aiohttp.ClientSession() as session:
            await get_status_for_all_domains(session=session, db_session=db_session)
            await asyncio.sleep(60 * 5)


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


@app.post("/add_domain", status_code=status.HTTP_201_CREATED)
async def post_domain(
    domain: Annotated[str, Body(embed=True)], db_session: db_connection
):
    try:
        new_domain = await add_domain(session=db_session, domain=domain)
        return new_domain
    except DomainAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Domain already exists")


@app.get("/examinations/{domain}", status_code=status.HTTP_200_OK)
async def get_domain_examinations(domain: str, db_session: db_connection):
    try:
        domain_examinations = await get_domain_with_examinations(
            domain=domain, session=db_session
        )
        return domain_examinations
    except NoDomainFoundError:
        raise HTTPException(status_code=404, detail="Domain not found")

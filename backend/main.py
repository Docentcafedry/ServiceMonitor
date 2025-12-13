import asyncio
import logging
from http.client import HTTPException

import aiohttp
from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, status, HTTPException
from backend.db import engine, Base
from backend.middlewares import RequestLoggingMiddleware
from backend.service import get_status_for_all_domains
from backend.db import async_session
from backend.depends import db_connection
from backend.service import add_domain, get_domain_with_examinations, get_all_domains
from backend.exceptions import DomainAlreadyExistsError, NoDomainFoundError
from fastapi.middleware.cors import CORSMiddleware
from backend.utils import validate_url

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def wait():
    while True:
        async with aiohttp.ClientSession() as session:
            await get_status_for_all_domains(
                https_session=session, db_session_factory=async_session
            )
            await asyncio.sleep(60 * 5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        print("Successfully created db tables!")

    asyncio.create_task(wait())
    yield


app = FastAPI(
    title="My API",
    version="3.1.0",  # Your API version
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(RequestLoggingMiddleware, logger=logger)


@app.get("/domains", status_code=status.HTTP_200_OK)
async def get_domains(db_session: db_connection):
    domains = await get_all_domains(session=db_session)
    return domains


@app.post("/add_domain", status_code=status.HTTP_201_CREATED)
async def post_domain(
    domain: Annotated[str, Body(embed=True)], db_session: db_connection
):
    if not validate_url(domain):
        raise HTTPException(status_code=400, detail="Wrong URL")

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

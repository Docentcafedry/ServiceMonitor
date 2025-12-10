import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from main import app
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import text
from db import get_db_connection
from db import Base, add_domain_to_database


client = TestClient(app)


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # ensures SAME in-memory DB across all sessions
    future=True,
    echo=False,
)

async_session_test = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_test_db_connection():
    db = async_session_test()
    try:
        yield db
    finally:
        await db.close()


app.dependency_overrides[get_db_connection] = get_test_db_connection


@pytest.fixture(scope="session", autouse=True)
async def fake_db():

    db = async_session_test()
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield db
    finally:
        await db.close()


@pytest.fixture(scope="function")
async def db_session():
    session = async_session_test()
    yield session
    # Remove any data from database (even data not created by this session)
    await session.rollback()  # rollback the transactions

    # truncate all tables
    for table in reversed(Base.metadata.sorted_tables):
        await session.execute(text(f"DELETE FROM {table.name};"))
        await session.commit()

    await session.close()


@pytest.fixture(scope="function")
async def create_domain(db_session):
    domain = await add_domain_to_database("https://www.google.com/", db_session)
    return domain

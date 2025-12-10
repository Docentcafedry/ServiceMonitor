import pytest
import datetime
from unittest.mock import AsyncMock, patch

from service import (
    add_domain,
    get_all_domains,
    get_domain_with_examinations,
    get_service_status,
    get_status_for_all_domains,
)
from db import Domain as DomainModel
from db import add_domain_to_database
from schemas import Domain
from utils import FakeAiohttpSession
from sqlalchemy import text
from .conftest import async_session_test


async def test_add_domain(db_session):
    """Test adding a domain using service layer."""
    result = await add_domain("example.com", db_session)

    assert result is not None
    assert isinstance(result, Domain)
    assert result.domain == "example.com"

    # Check database
    domains = await db_session.execute(DomainModel.__table__.select())
    records = domains.fetchall()
    assert len(records) == 1


async def test_get_all_domains(db_session):
    """Test retrieving all domains (service wrapper)."""
    await add_domain_to_database("https://www.google.com/", db_session)
    await add_domain_to_database("https://www.yandex.ru/", db_session)

    result = await get_all_domains(db_session)

    assert len(result) == 2
    assert result[0].domain.startswith("https://") is False  # cleaned URL
    assert isinstance(result[0], Domain)


async def test_get_domain_with_examinations(db_session):
    """Test retrieving domain with related examinations."""
    # Create a domain
    domain = await add_domain_to_database("https://www.google.com/", db_session)

    # Create examinations manually
    from db import Examination as ExamModel

    exam = ExamModel(
        status_code=200,
        examination_time=datetime.datetime.now(),
        response_time=datetime.timedelta(milliseconds=123),
        domain_id=domain.id,
    )
    db_session.add(exam)
    await db_session.commit()

    # Service call
    result = await get_domain_with_examinations("google.com", db_session)

    assert result.id == domain.id
    assert len(result.examinations) == 1
    assert result.examinations[0].status_code == 200


async def test_get_service_status(db_session):
    """Test the service status checker using proper aiohttp mocking."""

    fake_session = FakeAiohttpSession(status=200)
    domain = Domain(id=1, domain="https://example.com/")

    result = await get_service_status(
        domain=domain,
        http_session=fake_session,
        db_session=db_session,
    )

    assert result.status_code == 200

    # Make sure DB insert happened
    rows = await db_session.execute(text("SELECT COUNT(*) FROM examinations"))
    assert rows.scalar() == 1


async def test_get_status_for_all_domains(db_session):
    """Test running status checks on all domains (parallel execution)."""

    # Insert two domains
    await add_domain_to_database("https://www.google.com/", db_session)
    await add_domain_to_database("https://www.yandex.ru/", db_session)

    # Mock aiohttp client
    fake_session = FakeAiohttpSession(status=200)

    await get_status_for_all_domains(
        https_session=fake_session, db_session_factory=async_session_test
    )

    # Should create 2 examinations
    rows = await db_session.execute(text("SELECT COUNT(*) FROM examinations"))
    count = rows.scalar()

    assert count == 2

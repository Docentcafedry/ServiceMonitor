import asyncio
import datetime

import pytest
from db import (
    add_domain_to_database,
    get_all_domains_from_db,
    add_examination_to_database,
    get_domain_and_examination_from_db,
)
from schemas import Examination


async def test_add_domain(db_session):
    new_domain = await add_domain_to_database("https://www.google.com/", db_session)

    all_domains = await get_all_domains_from_db(db_session)

    assert len(all_domains) == 1
    assert all_domains[0].domain == "https://www.google.com/"


async def test_add_examination(db_session, create_domain):
    await add_examination_to_database(
        Examination(
            status_code=200,
            examination_time=datetime.datetime.now(),
            response_time=datetime.timedelta(microseconds=23),
            domain_id=create_domain.id,
        ),
        db_session,
    )

    domain_with_examination = await get_domain_and_examination_from_db(
        domain="google.com", session=db_session
    )
    assert len(domain_with_examination.examinations) == 1
    assert domain_with_examination.examinations[0].domain_id == create_domain.id

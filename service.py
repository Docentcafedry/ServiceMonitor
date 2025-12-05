import asyncio
import datetime
from aiohttp.client import ClientSession
from schemas import Examination, Domain, DomainWithExaminations
from sqlalchemy.ext.asyncio import AsyncSession
from db import add_examination_to_database, get_all_domains_from_db


async def get_service_status(
    domain: Domain, session: ClientSession, db_session: AsyncSession
) -> Examination:
    time_now = datetime.datetime.now(datetime.timezone.utc)
    async with session.get(domain.domain) as response:
        end_time = datetime.datetime.now(datetime.timezone.utc)
        status_code = response.status
        examination_time = datetime.datetime.now(datetime.timezone.utc)
        response_time = end_time - time_now
        examination = Examination(
            status_code=status_code,
            examination_time=examination_time,
            response_time=response_time,
            domain_id=domain.id,
        )
        await add_examination_to_database(session=db_session, examination=examination)
        return examination


async def get_status_for_all_domains(session: ClientSession, db_session: AsyncSession):
    print("from func")
    domains = await get_all_domains_from_db(session=db_session)
    print(domains)
    if not domains:
        print("Domains database is empty")
        return
    domain_schemas = [
        Domain.model_validate({"id": int(domain.id), "domain": domain.domain})
        for domain in domains
    ]
    await asyncio.gather(
        *[
            get_service_status(domain=domain, session=session, db_session=db_session)
            for domain in domain_schemas
        ]
    )


async def add_domain(domain: str, session: AsyncSession):
    new_domain = await add_domain(domain=domain, session=session)
    return Domain.model_validate({"id": new_domain.id, "domain": new_domain.domain})


async def get_domain_with_examinations(domain: str, session: AsyncSession):
    domain = await get_domain_with_examinations(domain=domain, session=session)

    return DomainWithExaminations.model_validate(
        {"id": domain.id, "domain": domain.domain, "examinations": domain.examinations}
    )

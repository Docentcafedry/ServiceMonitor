import asyncio
import datetime
from aiohttp.client import ClientSession
from schemas import Examination, Domain, DomainWithExaminations, ExaminationDB
from sqlalchemy.ext.asyncio import AsyncSession
from db import (
    add_examination_to_database,
    get_all_domains_from_db,
    add_domain_to_database,
    get_domain_and_examination_from_db,
    get_db_connection,
)
from utils import clean_url


async def get_service_status(
    domain: Domain, http_session: ClientSession, db_session: AsyncSession
) -> Examination:
    time_now = datetime.datetime.now(datetime.timezone.utc)
    async with http_session.get(domain.domain) as response:
        end_time = datetime.datetime.now(datetime.timezone.utc)
        status_code = response.status
        examination_time = datetime.datetime.now()
        response_time = end_time - time_now
        examination = Examination(
            status_code=status_code,
            examination_time=examination_time,
            response_time=response_time,
            domain_id=domain.id,
        )
        await add_examination_to_database(session=db_session, examination=examination)
        return examination


async def get_status_for_all_domains(https_session: ClientSession, db_session_factory):
    async with db_session_factory() as db_session:
        domains = await get_all_domains_from_db(session=db_session)
    print(domains)
    if not domains:
        print("Domains database is empty")
        return
    domain_schemas = [
        Domain.model_validate({"id": int(domain.id), "domain": domain.domain})
        for domain in domains
    ]

    async def process(domain):

        async with db_session_factory() as db_sess:
            return await get_service_status(
                domain=domain, http_session=https_session, db_session=db_sess
            )

    await asyncio.gather(*[process(domain=domain) for domain in domain_schemas])


async def add_domain(domain: str, session: AsyncSession) -> Domain:
    new_domain = await add_domain_to_database(domain=domain, session=session)
    return Domain.model_validate({"id": new_domain.id, "domain": new_domain.domain})


async def get_domain_with_examinations(
    domain: str, session: AsyncSession
) -> DomainWithExaminations:
    domain = await get_domain_and_examination_from_db(domain=domain, session=session)
    domain_with_exams = DomainWithExaminations.model_validate(
        {
            "id": domain.id,
            "domain": domain.domain,
            "examinations": [
                ExaminationDB.model_validate(
                    (
                        {
                            "id": examination.id,
                            "examination_time": examination.examination_time,
                            "response_time": examination.response_time,
                            "domain_id": examination.domain_id,
                            "status_code": examination.status_code,
                        }
                    )
                )
                for examination in domain.examinations
            ],
        }
    )

    return domain_with_exams


async def get_all_domains(session: AsyncSession):
    domains = await get_all_domains_from_db(session=session)
    domain_schemas = [
        Domain.model_validate(
            {"id": int(domain.id), "domain": clean_url(domain.domain)}
        )
        for domain in domains
    ]
    return domain_schemas

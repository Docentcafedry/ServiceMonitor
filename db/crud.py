from sqlalchemy.ext.asyncio import AsyncSession
from .models import Domain, Examination as ExaminationModel
from exceptions import (
    DomainAlreadyExistsError,
    ExaminationCreateDBError,
    NoDomainFoundError,
)
from sqlalchemy.exc import IntegrityError, ArgumentError
from schemas import Examination
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload


async def add_domain_to_database(domain: str, session: AsyncSession):
    new_domain = Domain(domain=domain)
    session.add(new_domain)
    try:
        await session.commit()
    except IntegrityError:
        raise DomainAlreadyExistsError
    await session.flush()
    return new_domain


async def add_examination_to_database(examination: Examination, session: AsyncSession):
    new_examination = ExaminationModel(**examination.model_dump())
    session.add(new_examination)
    try:
        await session.commit()
    except ArgumentError:
        raise ExaminationCreateDBError


async def get_all_domains_from_db(session: AsyncSession):
    res: Result = await session.execute(statement=select(Domain))
    return res.scalars().all()


async def get_domain_and_examination_from_db(domain: str, session: AsyncSession):
    stmt = (
        select(Domain)
        .where(Domain.domain == domain)
        .options(joinedload(Domain.examinations))
    )
    result: Result = await session.execute(stmt)
    domain: Domain = result.scalar_one_or_none()
    if not domain:
        raise NoDomainFoundError
    return domain

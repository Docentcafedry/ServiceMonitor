import datetime
from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Domain(Base):
    __tablename__ = "domains"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    domain: Mapped[str] = mapped_column(String(60), unique=True)
    examinations: Mapped[List["Examination"]] = relationship(back_populates="domain")


class Examination(Base):
    __tablename__ = "examinations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status_code: Mapped[int] = mapped_column(Integer)
    examination_time: Mapped[datetime.datetime] = mapped_column(default=func.now())
    response_time: Mapped[datetime.timedelta] = mapped_column()
    domain_id: Mapped[int] = mapped_column(ForeignKey("domains.id"), nullable=False)
    domain: Mapped["Domain"] = relationship(back_populates="examinations")

import datetime

from pydantic import BaseModel
from typing import List


class Examination(BaseModel):
    status_code: int
    examination_time: datetime.datetime
    response_time: datetime.timedelta
    domain_id: int


class Domain(BaseModel):
    id: int
    domain: str


class DomainWithExaminations(Domain):
    examinations: List[Examination]

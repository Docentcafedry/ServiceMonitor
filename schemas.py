import datetime

from pydantic import BaseModel


class Examination(BaseModel):
    status_code: int
    examination_time: datetime.datetime
    response_time: datetime.timedelta
    domain_id: int

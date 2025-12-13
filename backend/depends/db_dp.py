from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db_connection

db_connection = Annotated[AsyncSession, Depends(get_db_connection)]

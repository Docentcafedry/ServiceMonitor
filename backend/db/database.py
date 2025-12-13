from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


from backend.config.settings import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=50,
    max_overflow=100,
    pool_timeout=30,
    pool_recycle=1800,
    pool_use_lifo=True,
)

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db_connection():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()

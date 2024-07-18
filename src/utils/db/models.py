import asyncio
from sqlalchemy import (
    MetaData,
    Integer,
    BigInteger,
    Float,
    String,
    Boolean,
    DateTime,
    JSON,
    TEXT,
    UniqueConstraint,
    TIME
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)
import datetime
from datetime import timedelta
from utils.config import DSN
from utils.logging.logger import logger

meta = MetaData()
Base = declarative_base(metadata=meta)

def get_engine():
    try:
        engine = create_async_engine(DSN)
        async_session = async_sessionmaker(engine)
        return async_session
    except ValueError as e:
        if 'invalid literal for int() with base 10: ':
            asyncio
            asyncio.run(logger.critical(f'Движок не создан, заполните config.py'))
            return None

class UserModel(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    full_name: Mapped[str] = mapped_column(String)
    join_time: Mapped[str] = mapped_column(DateTime(timezone=True))
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    welcome_notif_id: Mapped[int] = mapped_column(Integer, default=0)
    feature_notif_id: Mapped[int] = mapped_column(Integer, default=0)


async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(meta.create_all)
            await logger.info('✅ БД созданы')
    except Exception as e:
        if "already exists" in str(e):
            await logger.info('✅ БД уже существуют')
        else:
            await logger.critical(f'Databases crashed: {e}')


async def time_after_month(_time):
    one_month = timedelta(days=30)
    _time_after_month = _time + one_month
    return _time_after_month

    
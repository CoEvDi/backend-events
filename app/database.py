from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text
from sqlalchemy import (Table, Column, Integer, String, DateTime, Date, Time,
                        MetaData, ForeignKey)
from datetime import datetime

from .config import cfg

_engine = create_async_engine(cfg.DB_CONNECTION_STRING)
_metadata = MetaData()


events = Table('events', _metadata,
    Column('id', Integer, primary_key=True),
    Column('created_time', DateTime, default=datetime.utcnow, nullable=False),

    Column('title', String, nullable=False),
    Column('preview', String, nullable=False),
    Column('description', String, nullable=False),

    Column('start_date', Date, nullable=False),
    Column('end_date', Date, nullable=False),
    Column('start_time', Time, nullable=False),
    Column('end_time', Time, nullable=False),
    
    Column('location', String, nullable=False),
    Column('site_link', String, nullable=False),

    Column('additional_info', String, nullable=True),
    Column('guests_info', String, nullable=True)
)

participants = Table('participants', _metadata,
    Column('participation_id', Integer, primary_key=True),
    Column('event_id', None, ForeignKey('events.id')),
    Column('account_id', Integer, nullable=False),
    Column('role', String, nullable=False),
    Column('joined_time', DateTime, default=datetime.utcnow, nullable=False)
)


async def check_database():
    try:
        async with _engine.begin() as conn:
            answer = await conn.execute(text("SELECT version();"))
            print(f'Successfully connecting to database.\n{answer.first()}')
    except Exception as e:
        print(f'Failed to connect to database:\n{str(e)}')


async def recreate_tables():
    async with _engine.begin() as conn:
        print('Dropping existing tables - ', end='', flush=True)
        try:
            await conn.run_sync(_metadata.reflect)
            await conn.run_sync(_metadata.drop_all)
            print('OK')
        except Exception as e:
            print(f'Failed to drop tables.\n{str(e)}')

        print('Creating tables - ', end='', flush=True)
        await conn.run_sync(_metadata.create_all)
        print('OK')

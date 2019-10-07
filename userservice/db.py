import logging
import uuid

import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, String,
    DateTime, func, select)
from sqlalchemy.dialects.postgresql import UUID

__all__ = ['init_pg', 'close_pg', 'user']

LOGGER = logging.getLogger(__name__)

USER_NOT_EXISTS_MSG = "User with id: {} does not exist"

meta = MetaData()

user = Table(
    'user', meta,

    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('name', String, nullable=False),
    Column('email', String, nullable=False),
    Column('created_at', DateTime(timezone=True), server_default=func.now()),
    Column('updated_at', DateTime(timezone=True), onupdate=func.now())
)


class RecordNotFound(Exception):
    """Requested record was not found in the database"""


async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


async def get_all_users(conn):
    cursor = await conn.execute(select([user.c.id, user.c.name, user.c.email]))
    records = await cursor.fetchall()
    return [dict(u) for u in records]


async def create_user(conn, user_name, user_email):
    result = await conn.execute(
        user.insert()
            .returning(user.c.id, user.c.name, user.c.email)
            .values(name=user_name, email=user_email))

    user_record = await result.first()
    LOGGER.info("User successfully inserted in the DB")
    return dict(user_record.items())


async def get_user(conn, user_id):
    result = await conn.execute(
        user.select(user.c.id, user.c.name, user.c.email)
            .where(user.c.id == user_id))
    user_record = await result.first()

    if not user_record:
        raise RecordNotFound(USER_NOT_EXISTS_MSG.format(user_id))

    LOGGER.info("User found in the DB")
    return dict(user_record.items())


async def update_user(conn, user_id, user_name, user_email):
    result = await conn.execute(
        user.update()
            .returning(user.c.id, user.c.name, user.c.email)
            .where(user.c.id == user_id)
            .values(name=user_name, email=user_email))
    user_record = await result.fetchone()
    if not user_record:
        raise RecordNotFound(USER_NOT_EXISTS_MSG.format(user_id))

    LOGGER.info("User successfully updated in the DB")
    return dict(user_record.items())


async def delete_user(conn, user_id):
    result = await conn.execute(
        user.delete()
            .where(user.c.id == user_id))
    user_record = await result.fetchone()
    if not user_record:
        raise RecordNotFound(USER_NOT_EXISTS_MSG.format(user_id))

    LOGGER.info("User successfully deleted from the DB")

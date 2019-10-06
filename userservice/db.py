import uuid

import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, String
)
from sqlalchemy.dialects.postgresql import UUID

__all__ = ['init_pg', 'close_pg', 'user']

USER_NOT_EXISTS_MSG = "User with id: {} does not exist"

meta = MetaData()

user = Table(
    'user', meta,

    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('name', String, nullable=False),
    Column('email', String, nullable=False)
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


async def create_user(conn, user_name, user_email):
    result = await conn.execute(
        user.insert()
            .returning(*user.c)
            .values(name=user_name, email=user_email))

    user_record = await result.first()
    return dict(user_record.items())


async def get_user(conn, user_id):
    result = await conn.execute(
        user.select()
            .where(user.c.id == user_id))
    user_record = await result.first()

    if not user_record:
        raise RecordNotFound(USER_NOT_EXISTS_MSG.format(user_id))

    return dict(user_record.items())


async def update_user(conn, user_id, user_name, user_email):
    result = await conn.execute(
        user.update()
            .returning(*user.c)
            .where(user.c.id == user_id)
            .values(name=user_name, email=user_email))
    user_record = await result.fetchone()
    if not user_record:
        raise RecordNotFound(USER_NOT_EXISTS_MSG.format(user_id))

    return dict(user_record.items())


async def delete_user(conn, user_id):
    result = await conn.execute(
        user.delete()
            .where(user.c.id == user_id))
    user_record = await result.fetchone()
    if not user_record:
        raise RecordNotFound(USER_NOT_EXISTS_MSG.format(user_id))

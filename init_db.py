from sqlalchemy import create_engine, MetaData

from userservice.db import user
from userservice.settings import BASE_DIR, get_config

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"

USER_CONFIG_PATH = BASE_DIR / 'config' / 'userservice.yaml'
USER_CONFIG = get_config(['-c', USER_CONFIG_PATH.as_posix()])

ADMIN_DB_URL = DSN.format(
    user='postgres', password='postgres', database='postgres',
    host=USER_CONFIG['postgres']['host'], port=5432
)

admin_engine = create_engine(ADMIN_DB_URL, isolation_level='AUTOCOMMIT')

USER_DB_URL = DSN.format(**USER_CONFIG['postgres'])
user_engine = create_engine(USER_DB_URL)


def setup_db(config):
    db_name = config['database']
    db_user = config['user']
    db_pass = config['password']

    conn = admin_engine.connect()

    # Using UUID functions
    conn.execute("CREATE EXTENSION IF NOT EXISTS \"pgcrypto\"")

    conn.execute("DROP DATABASE IF EXISTS %s" % db_name)
    conn.execute("DROP ROLE IF EXISTS %s" % db_user)

    conn.execute("CREATE USER %s WITH PASSWORD '%s'" % (db_user, db_pass))
    conn.execute("CREATE DATABASE %s ENCODING 'UTF8'" % db_name)
    conn.execute("GRANT ALL PRIVILEGES ON DATABASE %s TO %s" %
                 (db_name, db_user))

    conn.close()


def teardown_db(config):
    db_name = config['database']
    db_user = config['user']

    conn = admin_engine.connect()
    conn.execute("""
      SELECT pg_terminate_backend(pg_stat_activity.pid)
      FROM pg_stat_activity
      WHERE pg_stat_activity.datname = '%s'
        AND pid <> pg_backend_pid();""" % db_name)
    conn.execute("DROP DATABASE IF EXISTS %s" % db_name)
    conn.execute("DROP ROLE IF EXISTS %s" % db_user)
    conn.close()


def create_tables(engine=user_engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[user])


def drop_tables(engine=user_engine):
    meta = MetaData()
    meta.drop_all(bind=engine, tables=[user])


def sample_data(engine=user_engine):
    conn = engine.connect()
    conn.execute(user.insert(), [
        {'name': 'Bruce Wayne',
         'email': 'bruce@waynecorp.com'}
    ])

    conn.close()


if __name__ == '__main__':
    setup_db(USER_CONFIG['postgres'])
    create_tables(engine=user_engine)
    sample_data(engine=user_engine)
    # drop_tables()
    # teardown_db(config)

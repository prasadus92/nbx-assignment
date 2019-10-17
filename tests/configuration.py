import pytest

from init_db import (
    setup_db,
    teardown_db,
    create_tables,
    sample_data,
    drop_tables
)
from userservice.app import main
from userservice.settings import get_config


@pytest.fixture
async def cli(loop, test_client, db):
    app = await main()
    return await test_client(app)


@pytest.fixture(scope='module')
def db():
    test_config = get_config()

    setup_db(test_config['postgres'])
    yield
    teardown_db(test_config['postgres'])


@pytest.fixture
def tables_and_data():
    create_tables()
    sample_data()
    yield
    drop_tables()

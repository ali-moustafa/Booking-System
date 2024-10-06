import pytest

from booking_system.app import create_app


@pytest.fixture(scope='module')
def test_client():
    application = create_app()
    application.config['TESTING'] = True

    testing_client = application.test_client()

    ctx = application.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

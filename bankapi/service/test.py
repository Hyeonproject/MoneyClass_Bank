from typing import Generator
from tortoise.contrib.test import initializer, finalizer
import asyncio, pytest

def header_token(token):
    return {'Authorization': 'Bearer {}'.format(token)}

@pytest.fixture(scope='module')
def client() -> Generator:
    pass

@pytest.fixture(scope='session', autouse=True)
def initialize_tests(request):
    pass
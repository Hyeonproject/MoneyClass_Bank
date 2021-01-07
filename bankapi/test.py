import pytest, json
from httpx import AsyncClient

from tortoise.contrib.test import finalizer, initializer

from .main import app
from .service import key

__STUDENT_TOKEN = key.get_key('test_student_token')
__TEACHER_TOKEN = key.get_key('test_teacher_token')

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        response = await ac.get('/')
    assert response.status_code == 200
    assert response.json() == {'message' : '안녕하세요. 은행 API입니다.'}

# @pytest.fixture(scope='session', autouse=True)
# def initialize_tests(request):
#     initializer(['blogapi.models.model'], db_url=key.url, app_label='model')
#     request.addfinalizer(finalizer=finalizer)

initializer(['bankapi.models.model'], db_url=key.url, app_label='model')

@pytest.mark.asyncio
async def test_create_account():
    header = {'Authorization' : 'Bearer {}'.format(key.get_key('test_teacher_token'))}
    async with AsyncClient(app=app, base_url='http://test', headers=header) as ac:
        response = await ac.post('/account')

    assert response.status_code == 200
    response_json = json.dumps(response.json)
    assert response_json['user_email'] == 'sex@test.com'

@pytest.mark.asyncio
async def test_get_account():
    header = {'Authorization': 'Bearer {}'.format(key.get_key('test_teacher_token'))}
    async with AsyncClient(app=app, base_url='http://test', headers=header) as ac:
        response = await ac.get('/account')

finalizer()
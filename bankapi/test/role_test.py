'''
권한 관련 기능에 대한 테스트 코드
'''
from fastapi.testclient import TestClient
from tortoise.contrib.test import initializer, finalizer

from ..main import app
from ..service import key, test
from ..models import model

__STUDENT_TOKEN = key.get_key('test_student_token')
__TEACHER_TOKEN = key.get_key('test_teacher_token')

client = TestClient(app)
initializer(['bankapi.models.model'], db_url=key.url, app_label='model')

def test_read_roles_exception():
    # 데이터가 없을 경우
    response = client.get('/role')
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}

    # 권한 예외 테스트
    response = client.get('/role', headers=test.header_token(__STUDENT_TOKEN))
    assert response.status_code == 401
    assert response.json() == {'detail': '이 기능을 사용할 권한이 없습니다.'}

def test_read_roles():
    response = client.get('/role')
    assert response.status_code == 200

def test_create_role_exception():
    # 토큰 데이터가 없을 때
    response = client.post('/role')
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}

    #권한 문제일때
    response = client.post('/role', headers=test.header_token(__STUDENT_TOKEN))
    assert response.status_code == 401
    assert response.json() == {'detail': '이 기능을 사용할 권한이 없습니다.'}

def test_create_role():
    response = client.post('/role', headers=test.header_token(__TEACHER_TOKEN))
    assert response.status_code == 200
from fastapi.testclient import TestClient

from ..main import app
from ..service import key, test

__STUDENT_TOKEN = key.get_key('test_student_token')
__TEACHER_TOKEN = key.get_key('test_teacher_token')


client = TestClient(app)

def test_read_customers_exception():
    # 그냥 아무 데이터 없이 줬을 경우
    reseponse = client.get('/account')
    assert reseponse.status_code == 401
    assert reseponse.json() == {'detail': 'Not authenticated'}

    # 학생 권한일 경우
    reseponse = client.get('/account', headers=test.header_token(__STUDENT_TOKEN))
    assert reseponse.status_code == 401
    assert reseponse.json() == {'detail': '이 기능을 사용할 권한이 없습니다.'}

def test_read_customers():
    # 선생님 권한의 토큰을 제공한 경우
    reseponse = client.get('/account', headers=test.header_token(__TEACHER_TOKEN))
    assert reseponse.status_code == 202

def test_create_user_exception():
    # 역할이 있는지 확인 부터 해야함
    pass
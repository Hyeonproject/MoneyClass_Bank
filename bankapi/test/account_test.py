from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


#todo testcode에서 데이터베이스 연결을 해주어야 한다.

def test_create_user():
    response = client.post(
        '/account',
        json={
            'user_email':'testcode@test.com',
            'user_role':'ROLE_STUDENT'
        }
    )
    assert response.status_code == 307


def test_read_user():
    response = client.get('/account/hyeon@test.com')
    assert response.status_code == 200
    assert response.json() == {
        "created": "2021-01-19T07:51:40.485549+00:00",
        "id": "50a92079-dcae-4edc-abd5-fe1789283452",
        "email": "hyeon@test.com",
        "role": "ROLE_TEACHER"
    }
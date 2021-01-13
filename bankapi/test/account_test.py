from fastapi.testclient import TestClient

from ..main import app
from ..service import key
from ..service.test_service import jwt_make

__TEACHER_TOKEN = key.get_key('teacher_token')


client = TestClient(app)


def test_create_user():
    response = client.post(
        '/account',
        json={
            'user_email': 'testing@test.com',
            'user_role': 'ROLE_TEACHER'
        }
    )
    assert response.status_code == 200
    user_json = response.json()
    assert user_json['email'] == 'testing@test.com'
    assert user_json['role'] == 'ROLE_TEACHER'


def test_read_users():
    response = client.get(
        '/account',
        headers= jwt_make(__TEACHER_TOKEN)
    )

    assert response.status_code == 200

def test_read_user():
    response = client.get(
        '/account/testing@test.com',

    )
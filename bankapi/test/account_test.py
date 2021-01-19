from fastapi.testclient import TestClient
from typing import Generator
from tortoise.contrib.test import initializer, finalizer
import pytest, asyncio

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
    assert response.status_code == 307
    # json 값을 읽어오지 못함 나도 모르겠음.


def test_read_users():
    response = client.get(
        '/account',
        headers = jwt_make(__TEACHER_TOKEN)
    )
    assert response.status_code == 200

def test_read_user():
    response = client.get(
        '/account/hyeon@test.com'
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['email'] == 'testing@test.com'

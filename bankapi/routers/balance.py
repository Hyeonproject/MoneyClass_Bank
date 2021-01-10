from fastapi import APIRouter

router = APIRouter(
    prefix='/balance',
    tags=['balance'],
    responses={404: {'description': 'Not found'}},
)

# 잔액 조회

# 잔액 조회

# 잔액 조회
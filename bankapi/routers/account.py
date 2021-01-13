from fastapi import APIRouter, Depends, HTTPException

from ..schemas.account import CreateUser, Status
from ..models.model import Customers, Customers_Pydantic, Accounts
from ..dependencies import token_role_filter

router = APIRouter(
    prefix='/account',
    tags=['account'],
    responses={404: {'description': 'Not found'}},
)


@router.post('/')
async def create_user(user_data: CreateUser):
    # customer 데이터 만들기
    customer_data = await Customers.create(email=user_data.user_email, role=user_data.user_role)
    # account 계좌 생성하기
    await Accounts.create(customer_id=customer_data.pk)
    return Customers_Pydantic.from_tortoise_orm(customer_data)


@router.get('/', dependencies=[Depends(token_role_filter)])
async def read_users():
    return await Customers_Pydantic.from_queryset(Customers.all())

@router.get('/{user_email}')
async def read_user(user_email: str):
    return Customers_Pydantic.from_queryset_single(Customers.get(email=user_email))
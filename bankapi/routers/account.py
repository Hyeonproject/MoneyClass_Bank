from fastapi import APIRouter, Depends, HTTPException

from ..schemas.account import User, Status
from ..models.model import Customers, Customers_Pydantic, Accounts
from ..dependencies import token_role_filter

router = APIRouter(
    prefix='/account',
    tags=['account'],
    responses={404: {'description': 'Not found'}},
)


@router.post('/')
async def create_user(user_data: User):
    """
    계좌와 유저를 만들어줍니다.
    :param user_data:
    :return:
    """
    # customer 데이터 만들기
    customer_data = await Customers.create(email=user_data.user_email, role=user_data.user_role)
    # account 계좌 생성하기
    await Accounts.create(id=customer_data.pk)
    return Customers_Pydantic.from_tortoise_orm(customer_data)


@router.get('/', dependencies=[Depends(token_role_filter)])
async def read_users():
    """
    유저들의 정보를 다 가져옵니다. 계좌 정보는 가져오지 않습니다.
    :return:
    """
    return await Customers_Pydantic.from_queryset(Customers.all())


@router.get('/{user_email}')
async def read_user(user_email: str):
    """
    유저의 정보를 가져옵니다. 계좌 정보는 가져오지 않습니다.
    :param user_email:
    :return:
    """
    return Customers_Pydantic.from_queryset_single(Customers.get(email=user_email))


@router.put('/{user_email}', response_model=Customers_Pydantic)
async def update_user(user_email: str, user: User):
    await Customers.filter(email=user_email).update(**user.dict(exclude_unset=True))
    return await Customers_Pydantic.from_queryset_single(Customers.get(email=user_email))


@router.delete('/{user_email}', response_model=Status, dependencies=[Depends(token_role_filter)])
async def delete_user(user_email: str):
    delete_count = await Accounts.filter(email=user_email).delete()
    if not delete_count:
        raise HTTPException(status_code=404, detail=f'{user_email}을 찾지 못했다.')
    return Status(message=f'{user_email}이 삭제되었습니다.')
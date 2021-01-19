from fastapi import APIRouter, Depends, HTTPException

from ..schemas.account import User, Status
from ..models.model import Customers, Accounts, Accounts_Pydantic, Customers_Pydantic
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
    """
    # customer 데이터 만들기
    await Customers.create(email=user_data.user_email, role=user_data.user_role)
    account_data = await Accounts.create(customer_email_id=user_data.user_email)
    return await Accounts_Pydantic.from_tortoise_orm(account_data)


@router.get('/', dependencies=[Depends(token_role_filter)])
async def read_users():
    """
    유저들의 정보를 다 가져옵니다. 계좌 정보는 가져오지 않습니다.
    """
    return await Customers_Pydantic.from_queryset(Customers.all())


@router.get('/{user_email}', response_model=Customers_Pydantic)
async def read_user(user_email: str):
    """
    이메일을 입력해서 조회를 가능합니다. 계좌 정보는 가져오지 않습니다.
    """
    return await Customers_Pydantic.from_queryset_single(Customers.get(email=user_email))


@router.put('/{user_email}', response_model=Customers_Pydantic)
async def update_user(user_email: str, user: User):
    """
    파일의 이메일과 내용을 수정합니다. 계좌의 잔액은 수정하지 않습니다.
    """
    user_data = Customers.filter(email=user_email)
    if (user.user_email is None) and (user.user_role is None):
        raise HTTPException(status_code=403, detail='데이터가 없습니다.')
    elif user.user_email is None:
        await user_data.update(role=user.user_role)
        return await Customers_Pydantic.from_queryset_single(Customers.get(email=user_email))
    elif user.user_role is None:
        await user_data.update(email=user.user_email)
        return await Customers_Pydantic.from_queryset_single(Customers.get(email=user.user_email))
    else:
        await user_data.update(email=user.user_email, role=user.user_role)
        return await Customers_Pydantic.from_queryset_single(Customers.get(email=user.user_email))


@router.delete('/{user_email}', response_model=Status, dependencies=[Depends(token_role_filter)])
async def delete_user(user_email: str):
    """
    이메일의 토대로 계정 데이터 삭제합니다.
    """
    delete_count = await Customers.filter(email=user_email).delete()
    if not delete_count:
        raise HTTPException(status_code=404, detail=f'{user_email}을 찾지 못했다.')
    return Status(message=f'{user_email}이 삭제되었습니다.')
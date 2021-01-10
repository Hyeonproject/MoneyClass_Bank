from fastapi import APIRouter, Depends, HTTPException

from ..schemas.account import CreateUser, Status
from ..models.model import Customers, Customers_Pydantic, Accounts, Accounts_Pydantic
from ..dependencies import token_role_filter

router = APIRouter(
    prefix='/account',
    tags=['account'],
    responses={404: {'description': 'Not found'}},
)

@router.get('/', dependencies=[Depends(token_role_filter)])
async def read_customers():
    '''
    고객의 데이터를 가져옵니다. 데이터에 계좌 잔액도 확인할 수 있게 만듭니다.
    '''
    return await Customers_Pydantic.from_queryset(Customers.all())

@router.get('/{user_email}', response_model=Customers_Pydantic)
async def get_customer(user_email: str):
    '''
    고객의 이메일을 가지고 고객의 데이터를 조회한다.
    '''
    return await Customers_Pydantic.from_queryset_single(Customers.get(customer_email=user_email))

@router.post('/')
async def create_user(user_data: CreateUser):
    # Customer에 데이터를 추가 한다.
    customer_data = await Customers.create(customer_email=user_data.user_email, role_id=user_data.user_role)
    # Account에 데이터를 추가 한다.
    account_data = await Accounts.create(balance=0, customer_id=customer_data.pk)

    return Customers_Pydantic.from_tortoise_orm(customer_data)

@router.delete('/{user_email}', dependencies=[Depends(token_role_filter)])
async def delete_user(user_email: str):
    '''
    유저와 계좌를 삭제한다. 유저가 삭제되면 계좌 삭제
    '''
    delete_count = await Customers.filter(customer_email=user_email).delete()
    if not delete_count:
        raise HTTPException(status_code=404, detail='사용자의 데이터를 찾을 수 없습니다.')
    return Status(message=f'{user_email}이 삭제되었습니다.')
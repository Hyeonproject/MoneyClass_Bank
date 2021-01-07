from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ..models.model import Account, Account_Pydantic, AccountIn_Pydantic
from ..schemas import account, token
from ..service.token_service import get_token
import pay, balance

router = APIRouter(
    prefix='/account',
    tags=['account'],
    responses={404: {'description': 'Not found'}},
)

router.include_router(pay.router)
router.include_router(balance.router)

@router.get('/', response_model=List[Account_Pydantic], tags=['admin', 'teacher'])
async def get_accounts(token_data: token.TokenData = Depends(get_token)):
    '''
    전체 리스트를 가져오는 기능이다.
    '''
    if token_data.user_role != 'ROLE_TEACHER' or token_data.user_role != 'ROLE_ADMIN':
        raise HTTPException(status_code=402, detail='이 기능을 사용할 권한이 없습니다.')
    return await Account_Pydantic.from_queryset(Account.all())

@router.get('/{user_email}', response_model=Account_Pydantic)
async def get_account(user_email: str):
    '''
    계좌 하나를 찾아서 조회하는 기능입니다.
    '''
    return await Account_Pydantic.from_queryset_single(Account.get(email=user_email))

@router.post('/', response_model=Account_Pydantic)
async def create_account(account: AccountIn_Pydantic):
    '''
    계좌를 만드는 기능입니다. 토큰이 필요합니다.
    '''
    token_data = await Account.create(**account.dict(exclude_unset=True))
    return await Account_Pydantic.from_tortoise_orm(token_data)

@router.delete('/{user_email}', response_model=account.Status, tags=['admin', 'teacher'])
async def delete_account(
    user_email: str,
    token_data: token.TokenData = Depends(get_token)
):
    '''
    계좌를 제거하는 기능입니다.
    '''
    if token_data.user_role != 'ROLE_TEACHER' or token_data.user_role != 'ROLE_ADMIN':
        raise HTTPException(status_code=403, detail='이 기능을 사용할 권한이 없습니다.')
    delete_count = await Account.filter(email=user_email).delete()
    if not delete_count:
        raise HTTPException(status_code=404, detail='사용자의 데이터를 찾을 수 없습니다.')
    return account.Status(message=f'{user_email}이 삭제되었다.')

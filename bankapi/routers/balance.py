from fastapi import APIRouter, Depends, HTTPException

from ..models.model import Account, Account_Pydantic, AdminLog, AdminLog_Pydantic
from ..schemas import account, token
from ..service.token_service import get_token

router = APIRouter(
    prefix='/balance',
    tags=['balance'],
    responses={404: {'description': 'Not found'}},
)

@router.put('/', tags=['admin', 'teacher'])
async def update_balance(
        update_data: account.UpdateBalance,
        token_data: token.TokenData = Depends(get_token)
):
    '''
    토큰에 있는 역할 데이터와 이메일을 가져와서 계좌를 가져온 뒤에 계좌의 잔액을 교환합니다.
    '''
    # 조건 확인
    if token_data.user_role != 'ROLE_TEACHER' or token_data.user_role != 'ROLE_ADMIN':
        raise HTTPException(status_code=402, detail='이 기능을 사용할 권한이 없습니다.')

    # 계좌가 있는지 확인
    update_user = await Account_Pydantic.from_queryset_single(Account.get(email=update_data.user_email))
    if update_user is None:
        return HTTPException(status_code=418, detail='유저의 값이 저장되어 있지 않습니다.')

    # 데이터 값 변경
    await Account.filter(email=update_data.user_email).update(balances=update_data.balance)

    # 관리자 사용 내역에 등록하기
    admin_log = await AdminLog.create(role=token_data.user_role, usage_details='update_balance',
                                      note=update_data.note)
    return AdminLog_Pydantic.from_tortoise_orm(admin_log)
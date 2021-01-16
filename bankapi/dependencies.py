from fastapi import HTTPException, Depends

from .schemas.balance import PaymentIn
from .schemas.token import TokenData
from .service.token_service import get_token
from .service.key import get_key


async def payment(pay: PaymentIn):
    if pay is None:
        raise HTTPException(status_code=400, detail='필요한 값이 없습니다.')
    elif pay.amount is None:
        raise HTTPException(status_code=400, detail='거래 금액이 입력되어 있지 않습니다.')
    elif pay.amount <= 0:
        raise HTTPException(status_code=400, detail='거래 금액이 음수 또는 0입니다.')
    elif pay.transfer_email is None:
        raise HTTPException(status_code=400, detail='받는 사람이 입력되어있지 않습니다.')
    elif pay.deposit_email is None:
        raise HTTPException(status_code=400, detail='보내는 사람이 입력되어있지 않습니다.')


async def token_role_filter(token_data: TokenData = Depends(get_token)):
    if token_data.user_role[0] != get_key('role_teacher') and token_data.user_role[0] != get_key('role_admin'):
        raise HTTPException(status_code=401, detail='이 기능을 사용할 권한이 없습니다.')

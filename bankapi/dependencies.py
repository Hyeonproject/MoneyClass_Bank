from fastapi import HTTPException

from .schemas.account import Payment

async def payment(payment : Payment):
    if payment is None:
        raise HTTPException(status_code=400, detail='필요한 값이 없습니다.')
    elif payment.amount is None:
        raise HTTPException(status_code=400, detail='거래 금액이 입력되어 있지 않습니다.')
    elif payment.amount <= 0:
        raise HTTPException(status_code=400, detail='거래 금액이 음수 또는 0입니다.')
    elif payment.receiver is None:
        raise HTTPException(status_code=400, detail='받는 사람이 입력되어있지 않습니다.')
    elif payment.user_email is None:
        raise HTTPException(status_code=400, detail='보내는 사람이 입력되어있지 않습니다.')
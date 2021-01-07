from fastapi import Depends, APIRouter, HTTPException

from ..dependencies import Payment
from ..models.model import Account, Account_Pydantic, Transcation_Pydantic, Transaction
from ..schemas import account

router = APIRouter(
    prefix='/pay',
    tags=['pay'],
    responses={404: {'description': 'Not found'}},
    dependencies=[Depends(Payment)],
)

@router.put('/{user_email}')
async def pay(user_email: str, payment: account.Payment):
    '''
    계좌 이체를 하는 기능입니다.
    '''
    user_data = await Account_Pydantic.from_queryset_single(Account.get(email=user_email))
    if user_data is None:
        raise HTTPException(status_code=418, detail='조회한 데이터가 없습니다.')
    amount = user_data.balances - payment.amount
    if amount < 0:
        raise HTTPException(status_code=418, detail='잔액이 부족합니다.')

    await Account.filter(id=user_data.id).update(balances=amount)

    receiver_data = await Account_Pydantic.from_queryset_single(Account.get(email=payment.receiver))
    await Account.filter(email=payment.receiver).update(balances=receiver_data.balances + payment.amount)

    transaction = await Transaction.create(account_id=user_data.id, amount=payment.amount,
                                           receiver=payment.receiver, note=payment.note)
    return await Transcation_Pydantic.from_tortoise_orm(transaction)
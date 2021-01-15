from fastapi import APIRouter, HTTPException, Depends
from tortoise.exceptions import BaseORMException, OperationalError
from tortoise.transactions import atomic, in_transaction

from ..models.model import Customers, Accounts, Accounts_Pydantic
from ..schemas.balance import BalanceOut, PaymentIn
from ..dependencies import payment

router = APIRouter(
    prefix='/balance',
    tags=['balance'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/')
async def read_balances():
    return Accounts_Pydantic.from_queryset(Accounts.all())


@router.get('/{user_email}', response_model=BalanceOut)
async def read_balance(user_email: str):
    try:
        customer = await Customers.get(email=user_email)
        account = await Accounts.get(customer_id=customer.pk)
    except BaseORMException:
        raise HTTPException(status_code=404, detail='데이터베이스 오류입니다.')

    output = BalanceOut(
        user_email=customer.email,
        user_role=customer.role,
        balance=account.balance,
        customer_id=customer.pk,
        account_id=account.pk
    )
    return output


@router.post('/pay', dependencies=[Depends(payment)])
async def pay(pay_data: PaymentIn):
    try:
        async with in_transaction() as
    transfer_user = await Customers.get(email=pay_data.transfer_user)
    deposit_user = await Customers.get(email=pay_data.deposit_user)

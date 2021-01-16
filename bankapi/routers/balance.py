from fastapi import APIRouter, HTTPException, Depends
from tortoise.exceptions import BaseORMException, OperationalError
from tortoise.transactions import in_transaction
from tortoise.expressions import F

from ..models.model import Customers, Accounts, Accounts_Pydantic, Transcations, Transcations_Pydantic
from ..schemas.balance import BalanceOut, PaymentIn
from ..dependencies import payment, token_role_filter

router = APIRouter(
    prefix='/balance',
    tags=['balance'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/')
async def read_balances():
    return await Accounts_Pydantic.from_queryset(Accounts.all())


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
        customer_id=customer.id,
        account_id=customer.id
    )
    return output


@router.post('/pay', dependencies=[Depends(payment)])
async def pay(pay_data: PaymentIn):
    """
    계좌 이체 기능입니다.
    기존에 자신과 보낼 사람의 데이터를 입력받고 처리하는 역할을 수행합니다.
    """
    try:
        transfer_user = await Customers.get(email=pay_data.transfer_email)
        deposit_user = await Customers.get(email=pay_data.deposit_email)
        transfer_account = await Accounts.get(customer_id=transfer_user.pk)
        # deposit_account = await Accounts.get(customer_id=deposit_user.pk)

        # 계좌에 있는 데이터 값 확인하기
        if transfer_account.balance <= pay_data.amount:
            raise HTTPException(status_code=404, detail=f'{pay_data.amount}의 돈이 있지 않습니다.')

        async with in_transaction() as connection:
            await Accounts.filter(customer_id=transfer_user.pk).update(
                balance = F('balance') - pay_data.amount
            )
            # await Accounts.filter(customer_id=deposit_user.pk).update(
            #     balance=deposit_account.balance + pay_data.amount
            # )
            await Accounts.filter(customer_id=deposit_user.pk).update(
                balance = F('balance') + pay_data.amount
            )
            transcation = await Transcations.create(
                amount=pay_data.amount,
                account_id=transfer_account.pk,
                customer_id=deposit_user.pk,
                trans_type=1, # 1번은 일반 이체
            )
    except OperationalError:
        raise HTTPException(status_code=404,detail='이체 도중의 문제가 발생했습니다.')

    return Transcations_Pydantic.from_orm(transcation)


# 월급 주는 기능
@router.post('/payday/{amount}', dependencies=[Depends(token_role_filter)])
async def payday(amount: int):
    """
    전체 월급을 주는 기능입니다. 월급을 amount 값을 입력하면 다음과 같이 사용할 수 있습니다.
    이 기능은 토큰값에서 권한이 있어야 사용 가능합니다.
    """
    await Accounts.all().update(balance = F('balance') + amount)
    return await Accounts_Pydantic.from_queryset(Accounts.all())
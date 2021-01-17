from fastapi import APIRouter, HTTPException, Depends
from tortoise.exceptions import BaseORMException, OperationalError
from tortoise.transactions import in_transaction
from tortoise.expressions import F
import uuid

from ..models.model import Customers, Accounts, Accounts_Pydantic, Transcation, Transcations_Pydantic
from ..schemas.balance import BalanceOut, PayIn
from ..dependencies import payment, token_role_filter

router = APIRouter(
    prefix='/balance',
    tags=['balance'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/')
async def read_balances():
    """
    전체 계좌를 다 확인하는 기능입니다.
    """
    return await Accounts_Pydantic.from_queryset(Accounts.all())


@router.get('/{user_email}', response_model=BalanceOut)
async def read_balance(user_email: str):
    """
    이메일을 통해서 자신의 계좌와 계정을 확인할 수 있습니다.
    """
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
async def payment(pay: PayIn):
    """
    계좌 이체 기능입니다.
    기존에 자신과 보낼 사람의 데이터를 입력받고 처리하는 역할을 수행합니다.
    """
    # 액수가 부족한지 검사하기
    transfer_customer = await Customers.get(email=pay.transfer_email)
    transfer_account = await Accounts.get(customer_id=transfer_customer.pk)

    if transfer_account.balance < pay.amount:
        raise HTTPException(status_code=400, detail='잔액이 부족해서 이체 불가능')
    # 돈 보내는 트랜잭션 + 기록
    try:
        async with in_transaction() as connection:
            await Accounts.filter(customer_id=transfer_customer.pk).update(
                balance=F('balance') - pay.amount
            )
            deposit_customer = await Customers.get(email=pay.deposit_email)
            await Accounts.filter(customer_id=deposit_customer.pk).update(
                balance=F('balance') + pay.amount
            )
            transcation_data = await Transcation.create(
                amount=pay.amount,
                account_id=transfer_account.pk,
                customer_id=deposit_customer.pk,
                trans_type_id=1,
                using_db=connection,
            )
    except OperationalError:
        raise HTTPException(status_code=400, detail='이체 도중 문제가 생겼습니다.')
    # 출력
    return await Transcations_Pydantic.from_tortoise_orm(transcation_data)


# 월급 주는 기능
@router.post('/payday/{amount}', dependencies=[Depends(token_role_filter)])
async def payday(amount: int):
    """
    전체 월급을 주는 기능입니다. 월급을 amount 값을 입력하면 다음과 같이 사용할 수 있습니다.
    이 기능은 토큰값에서 권한이 있어야 사용 가능합니다.
    """
    try:
        async with in_transaction() as connection:
            await Accounts.all().update(balance=F('balance') + amount)
            admin_customer = await Customers.get(email='admin@server.com')
            admin_account = await Accounts.get(customer_id=admin_customer.pk)
            await Transcation.create(
                amount=amount,
                account_id=admin_account.pk,
                customer_id=admin_customer.pk,
                trans_type_id=2,  # 월급 입금
                using_db=connection
            )
    except OperationalError:
        raise HTTPException(status_code=400, detail='월급 주는 도중에 문제가 발생했습니다.')

    return await Accounts_Pydantic.from_queryset(Accounts.all())
from fastapi import APIRouter, HTTPException, Depends
from tortoise.exceptions import BaseORMException, OperationalError
from tortoise.transactions import in_transaction
from tortoise.expressions import F

from ..models.model import Customers, Accounts, Accounts_Pydantic,\
    Transcation, Transcations_Pydantic, PayDay, PayDay_Pydantic
from ..schemas.balance import BalanceOut, PayIn
from ..dependencies import payment, token_role_filter

router = APIRouter(
    prefix='/balance',
    tags=['balance'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/', dependencies=[Depends(token_role_filter)])
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
        account = await Accounts.get(customer_email_id=customer.email)
    except BaseORMException:
        raise HTTPException(status_code=400, detail='데이터베이스를 찾는 도중 문제가 발생했습니다.')

    output = BalanceOut(
        user_email=customer.email,
        user_role=customer.role,
        balance=account.balance,
        customer_id=customer.id,
        account_id=account.id
    )
    return output


@router.post('/pay', dependencies=[Depends(payment)])
async def payment(pay: PayIn):
    """
    계좌 이체 기능입니다.
    기존에 자신과 보낼 사람의 데이터를 입력받고 처리하는 역할을 수행합니다.
    """
    # 액수가 부족한지 검사하기
    transfer_account = await Accounts.get(customer_email_id=pay.transfer_email)

    if transfer_account.balance < pay.amount:
        raise HTTPException(status_code=400, detail='잔액이 부족해서 이체 불가능')
    # 돈 보내는 트랜잭션 + 기록
    try:
        async with in_transaction() as connection:
            await Accounts.filter(customer_email_id=pay.transfer_email).update(
                balance=F('balance') - pay.amount
            )
            await Accounts.filter(customer_email_id=pay.deposit_email).update(
                balance=F('balance') + pay.amount
            )
            transcation_data = await Transcation.create(
                amount=pay.amount,
                transfer_email_id=pay.transfer_email,
                deposit_email_id=pay.deposit_email,
                trans_type_id='일반이체',
                using_db=connection,
            )
    except OperationalError:
        raise HTTPException(status_code=400, detail='이체 도중 문제가 생겼습니다.')
    # 출력
    return await Transcations_Pydantic.from_tortoise_orm(transcation_data)


@router.post('/payday/{amount}', dependencies=[Depends(token_role_filter)])
async def payday(amount: int):
    """
    월급을 주거나 세금을 전체다 걷어야할 때 사용합니다.
    음수로 값을 넣을 경우 음수로 작동합니다.
    관리자 또는 선생님의 권한을 가진 토큰이 필요합니다.
    """
    # 0 예외 처리
    if amount == 0:
        raise HTTPException(status_code=400, detail='0의 데이터는 입력을 받지 않습니다.')
    try:
        async with in_transaction() as connection:
            await Accounts.all().update(balance=F('balance') + amount)
            payday_data = await PayDay.create(
                amount=amount,
                trans_type_id='월급입금',
            )

    except OperationalError:
        raise HTTPException(status_code=400, detail='월급 주는 도중에 문제가 발생했습니다.')

    return await PayDay_Pydantic.from_tortoise_orm(payday_data)

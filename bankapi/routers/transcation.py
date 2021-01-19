from fastapi import APIRouter
from tortoise.query_utils import Q

from ..models.model import Transcation, Transcations_Pydantic, Customers, Accounts
from ..schemas.transcation import TranscationOut


router = APIRouter(
    prefix='/transcation',
    tags=['transcation'],
    responses={404: {'description': 'Not found'}},
)

# 거래 내역 조회
@router.get('/')
async def read_transcations():
    """
    거래 내역 테이블 전체 조회 입니다.
    """
    return await Transcations_Pydantic.from_queryset(Transcation.all())


@router.get('/{user_email}')
async def read_transcations(user_email: str):
    """
    이메일을 조회해서 이메일에 맞는 거래 내역을 분석합니다.
    """
    user_customer = await Customers.get(email=user_email)
    user_account = await Accounts.get(customer_id=user_customer.pk)
    user_queryset: TranscationOut = await Transcation.filter( Q(customer_id=user_customer.pk) | Q(account_id=user_account.pk))
    return user_queryset
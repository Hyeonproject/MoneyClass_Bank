from fastapi import APIRouter, Depends, HTTPException

from ..models.model import TranscationType, TranscationType_Pydantic
from ..schemas.transcation import TransTypeIn
from ..schemas.account import Status
from ..dependencies import token_role_filter

router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/transcation-type', dependencies=[Depends(token_role_filter)])
async def read_trans_types():
    """
    Transcation type 테이블 전체 조회
    """
    return await TranscationType_Pydantic.from_queryset(TranscationType.all())


@router.post('/transcation-type', dependencies=[Depends(token_role_filter)])
async def create_trans_type(trans: TransTypeIn):
    """
    Transcation type 생성
    """
    trans_type = await TranscationType.create(trans_type_name=trans.trans_type_name)
    return TranscationType_Pydantic.from_orm(trans_type)


@router.put('/transcation-type/{trans_id}', dependencies=[Depends(token_role_filter)])
async def update_trans_type(trans_id: int, trans: TransTypeIn):
    """
    transcation_type 수정할 수 있는 기능
    """
    trans_type = await TranscationType.filter(id=trans_id).update(trans_type_name=trans.trans_type_name)
    return await TranscationType_Pydantic.from_queryset_single(TranscationType.get(trans_type_name=trans.trans_type_name))


@router.delete('/transcation-type/{trans_id}', dependencies=[Depends(token_role_filter)])
async def delete_trans_type(tran_id: int):
    """
    transcation_type를 삭제할 수 있는 기능
    """
    delete_count = await TranscationType.filter(id=tran_id).delete()
    if not delete_count:
        raise HTTPException(status_code=404, detail=f'{tran_id} 번호의 데이터가 없다.')
    return Status(message=f'{tran_id}가 삭제되었습니다.')
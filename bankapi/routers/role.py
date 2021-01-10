from fastapi import APIRouter, Depends, HTTPException

from ..models.model import Roles, Role_Pydantic, RoleIn_Pydantic

from ..dependencies import token_role_filter

router = APIRouter(
    prefix='/role',
    tags=['role'],
    dependencies=[Depends(token_role_filter)],
    responses={404: {"description": "Not found"}},
)

@router.get('/')
async def read_roles():
    '''
    역할 테이블을 전체다 읽습니다.
    '''
    return await Role_Pydantic.from_queryset(Roles.all())

@router.post('/')
async def create_role(role_data: RoleIn_Pydantic):
    '''
    역할 테이블을 생성합니다.
    '''
    role = await Roles.create(**role_data.dict(exclude_unset=True))
    return await Role_Pydantic.from_tortoise_orm(role)

@router.put('/{role_id}', response_model=Role_Pydantic)
async def update_role(role_id: int, role: RoleIn_Pydantic):
    '''
    역할 테이블을 수정합니다.
    '''
    await Roles.filter(pk=role_id).update(**role.dict(exclude_unset=True))
    return await Role_Pydantic.from_queryset_single(Roles.get(pk=role_id))

@router.delete('/{role_id}')
async def delete_role(role_id: int):
    '''
    역할 테이블을 삭제합니다.
    '''
    delete_count = await Roles.filter(pk=role_id).delete()
    if not delete_count:
        raise HTTPException(status_code=404, detail=f'{role_id}규칙이 없습니다.')
    return {'message': f'{role_id}를 삭제했습니다.'}
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import List

from .key import get_key
from ..schemas.token import TokenData

__ALGORITHM = 'HS256'
__CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token_data')

async def get_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, get_key('token_key'), algorithms=[__ALGORITHM])
        user_email: str = payload['user_name']
        user_role: List = payload['authorities']
        if user_email is None:
            raise __CREDENTIALS_EXCEPTION
        if user_role is None:
            raise __CREDENTIALS_EXCEPTION
        token_data = TokenData(user_email=user_email, user_role=user_role)
    except JWTError:
        raise __CREDENTIALS_EXCEPTION
    return token_data
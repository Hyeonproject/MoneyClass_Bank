from pydantic import BaseModel
from typing import Optional


class Status(BaseModel):
    message: str


class UpdateBalance(BaseModel):
    user_email: str
    balance: int
    note: Optional[str] = None


class User(BaseModel):
    user_email: str
    user_role: Optional[str] = 'ROLE_STUDENT'

from pydantic import BaseModel
from typing import Optional

class Status(BaseModel):
    message: str

class Payment(BaseModel):
    user_email: str
    receiver: str
    amount: int
    note: Optional[str] = None

class UpdateBalance(BaseModel):
    user_email: str
    balance: int
    note: Optional[str] = None
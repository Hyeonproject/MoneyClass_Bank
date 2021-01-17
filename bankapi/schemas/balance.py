from pydantic import BaseModel
import uuid


class BalanceOut(BaseModel):
    user_email: str
    user_role: str
    balance: int
    customer_id: uuid.UUID
    account_id: uuid.UUID


class PayIn(BaseModel):
    transfer_email: str
    deposit_email: str
    amount: int


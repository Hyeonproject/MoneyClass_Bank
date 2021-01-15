from pydantic import BaseModel


class BalanceOut(BaseModel):
    user_email: str
    user_role: str
    balance: int
    customer_id: str
    account_id: str


class PaymentIn(BaseModel):
    transfer_user: str
    deposit_user: str
    amount: int

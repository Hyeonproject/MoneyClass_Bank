from pydantic import BaseModel


class TransTypeIn(BaseModel):
    trans_type_name: str


class TranscationOut(BaseModel):
    transfer_email: str
    deposit_email: str
    amount: int
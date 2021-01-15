from pydantic import BaseModel


class TransTypeIn(BaseModel):
    trans_type_name: str

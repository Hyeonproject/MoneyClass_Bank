from pydantic import BaseModel
from typing import List, Optional

class TokenData(BaseModel):
    user_email : str
    user_role : List
from dataclasses import dataclass
from pydantic import BaseModel


class DepositRequest(BaseModel):
    account_id: str
    user_id: str
    amount: int
    request_time: str


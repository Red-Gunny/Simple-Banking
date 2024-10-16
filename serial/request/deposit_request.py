from typing import Optional

from pydantic import BaseModel


class DepositRequest(BaseModel):
    account_id: str
    customer_id: str
    amount: str
    etc: Optional[str]
    request_time: str



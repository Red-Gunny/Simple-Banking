from pydantic import BaseModel


class DepositRequest(BaseModel):
    account_id: str
    customer_id: str
    amount: int
    request_time: str


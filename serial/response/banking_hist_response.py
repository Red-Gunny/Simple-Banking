from typing import List
from pydantic import BaseModel


class Banking(BaseModel):
    banking_dttm: str
    banking_amount: str
    after_balance: str
    banking_div : str
    etc: str


class BankingHistResponse(BaseModel):
    account_id: str
    customer_id: str
    search_from_dt: str
    search_to_dt: str
    banking_div: str
    request_time: str
    Bakings: List[Banking]



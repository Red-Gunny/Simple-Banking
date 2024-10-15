from pydantic import BaseModel

class WithdrawRequest:
    account_id: str
    user_id: str
    amount: str
    request_time: str


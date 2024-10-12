from dataclasses import dataclass

@dataclass
class Withdraw_Request:
    account_id: str
    user_id: str
    amount: str
    request_time: str


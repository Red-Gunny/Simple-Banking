from dataclasses import dataclass

@dataclass
class Deposit_Request:
    account_id: str
    user_id: str
    amount: str
    request_time: str


from pydantic import BaseModel

class DepositResponse(BaseModel):
    account_id: str
    customer_id: str
    proc_id: str
    stat_cd: str

    model_config = {
        'from_attributes': True  # ORM 객체로부터 변환 가능
    }

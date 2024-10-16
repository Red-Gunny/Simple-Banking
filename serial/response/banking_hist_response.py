from typing import List, Optional
from pydantic import BaseModel, Field, validator, field_validator


class Banking(BaseModel):
    banking_seq: int
    banking_dttm: str = Field(alias="proc_dttm")
    banking_amount: str = Field(alias="amount")
    after_balance: str = Field(alias="balance")
    banking_div : str = Field(alias="proc_div")
    etc: Optional[str] = Field(alias="etc")

    model_config = {
        'from_attributes': True  # ORM 객체로부터 변환 가능
    }

    # pydantic에 의해 처리되기 전에  아래 메소드를 수행한다.
    @field_validator('banking_amount', 'after_balance', mode='before')
    def convert_to_int(cls, value):
        if isinstance(value, int):
            return str(value)  # 문자열을 정수로 변환
        return value


class BankingHistResponse(BaseModel):
    account_id: str
    customer_id: str
    request_dttm: str
    banking_cnt : int
    Bakings: List[Banking]

    model_config = {
        'from_attributes': True  # ORM 객체로부터 변환 가능
    }



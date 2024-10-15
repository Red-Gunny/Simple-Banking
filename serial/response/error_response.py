from pydantic import BaseModel


class ErrorResponse(BaseModel):
    account_id: str
    customer_id: str
    error_cd: str
    error_reason: str




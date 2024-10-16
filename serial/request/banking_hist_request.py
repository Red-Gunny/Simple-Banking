from typing import Optional

from pydantic import BaseModel


class BankingHistRequest(BaseModel):
    account_id: str = None
    customer_id: str = None
    search_from_dt: Optional[str] = None
    search_to_dt: Optional[str] = None
    filter_action: Optional[str] = None
    request_dttm: str = None


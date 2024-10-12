from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

class AccountBase:
    __tablename__ = "account_base"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String)
    status = Column(String)
    customer_id = Column(String)
    balance: Column(Integer)
    etc = Column(String)
    created_a = Column(String)
    modified_at = Column(String)



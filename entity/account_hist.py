from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

class AccountHist:
    __tablename__ = "account_hist"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String)
    seq = Column(Integer)
    status = Column(String)
    customer_id = Column(String)
    balance: Column(Integer)
    etc = Column(String)
    created_at = Column(String)
    modified_at = Column(String)

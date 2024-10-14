
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class JobHist(Base):
    __tablename__ = "job_hist"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String)
    customer_id = Column(String)
    account_id = Column(String)
    job_div = Column(String)
    proc_stat_cd =  Column(String)
    amount = Column(String)
    request_dttm = Column(String)
    created_at = Column(String)
    modified_at = Column(String)


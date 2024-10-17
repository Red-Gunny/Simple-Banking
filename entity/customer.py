
from sqlalchemy import Column, Integer, String

class Customer:
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, autoincrement=True)

    customer_id = Column(String)
    status = Column(String)
    created_at = Column(String)
    modified_at = Column(String)

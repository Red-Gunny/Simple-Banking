from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

'''
계좌 기본 테이블 정의
ACCOUNT_BASE 테이블에 매핑되는 클래스
'''
class AccountBase(Base):
    __tablename__ = "account_base"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # {account_id, seq} 식별자
    account_id = Column(String)         # 계좌 식별 아이디

    customer_id = Column(String)        # 고객 식별 아이디
    balance = Column(Integer)           # 현재 잔액
    last_proc_dttm = Column(String)     # 최종 계좌 변경 일시

    created_at = Column(String)         # 데이터 생성 시각
    modified_at = Column(String)        # 데이터 수정 시각



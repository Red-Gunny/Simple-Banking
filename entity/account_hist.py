from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

'''
계좌 이력 테이블 정의
ACCOUNT_HIST 테이블에 매핑되는 클래스
'''
class AccountHist(Base):
    __tablename__ = "account_hist"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # {account_id, seq} 식별자
    account_id = Column(String)         # 계좌 식별 아이디
    seq = Column(Integer)               # 작업 순번 (계좌 별)

    customer_id = Column(String)        # 고객 식별 아이디
    proc_div = Column(String)           # 작업 구분 (입금 / 출금)
    proc_dttm = Column(String)          # 작업 일시
    amount = Column(Integer)            # 금액
    balance = Column(Integer)           # 작업 후 잔액
    etc = Column(String)                # 적요

    created_at = Column(String)         # 데이터 생성 시각
    modified_at = Column(String)        # 데이터 수정 시각



from datetime import datetime

from entity.account_base import AccountBase

'''
account_base 테이블에 저장
'''
class AccountBaseRepository:

    ## 고객 식별자에 해당하는 account 정보를 반환함
    def search_by_customer_Id(self, session, customer_id):
        accounts = session.query(AccountBase).filter(AccountBase.customer_id == customer_id).all()
        return accounts

    ## 계좌 식별자 해당하는 account 정보를 반환함
    def search_by_account_id(self, session, account_id):
        account = session.query(AccountBase).filter(AccountBase.account_id == account_id).one()
        return account

    def insert(self, session, account_base: AccountBase):
        session.add(account_base)
        session.commit()

    # 계좌 잔액 변경
    def update_balance_and_last_proc_dttm(self, session, account_id : str, amount : int):
        session.query(AccountBase).filter(AccountBase.account_id == account_id).update({
            AccountBase.balance: AccountBase.balance + amount       # 현재 잔액
            , AccountBase.last_proc_dttm: datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 최종 작업 일시
            , AccountBase.modified_at : datetime.now().strftime("%Y-%m-%d %H:%M:%S")    # 수정 일시
              })
        session.commit()



from entity.account_base import AccountBase

'''
account_base 테이블에 저장
'''
class AccountBaseRepository:

    def insert(self, session, account_base: AccountBase):
        session.add(account_base)
        session.commit()


    ## 고객번호에 해당하는 account 정보를 반환함
    def search_by_customer_Id(self, session, customer_id):
        accounts = session.query(AccountBase).filter(AccountBase.customer_id == customer_id).all()
        return accounts



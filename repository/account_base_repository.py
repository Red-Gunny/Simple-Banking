from entity.account_base import AccountBase

'''
account_base 테이블에 저장
'''
class AccountBaseRepository:

    def insert(self, session, account_base: AccountBase):
        session.add(account_base)
        session.commit()


    ## 결과 미조회 일 수도 있음
    def search_by_customer_Id(self, session, customer_id):
        #accounts = ccountBase.query.filter(AccountBase.customer_id == customer_id).all()
        accounts = session.query(AccountBase).filter(AccountBase.customer_id == customer_id).all()
        return accounts



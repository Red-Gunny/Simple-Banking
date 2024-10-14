from entity.account_base import AccountBase

'''
account_base 테이블에 저장
'''
class AccountBaseRepository:


    def insert(self, session, account_base: AccountBase):
        session.add(account_base)
        session.commit()


from entity.account_hist import AccountHist

'''
account_hist 테이블에 저장
'''
class AccountHistRepository:


    def insert(self, session, account_hist: AccountHist):
        session.add(account_hist)
        session.commit()


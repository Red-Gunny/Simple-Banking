from entity.account_hist import AccountHist

'''
account_hist 테이블에 저장
'''
class AccountHistRepository:

    def insert(self, session, account_hist: AccountHist):
        session.add(account_hist)
        session.commit()


    '''
    기간 및 입출금에 따라 거래 내역 조회
    '''
    def search_by_dttm_and_job_div(self, session, customer_id, account_id, from_dttm, to_dttm, proc_div):
        print("Repository 계층 인입")
        account_hist = session.query(AccountHist).filter(AccountHist.account_id == account_id, AccountHist.customer_id == customer_id)

        if from_dttm is not None:
            account_hist = session.query(AccountHist).filter(AccountHist.created_at >= from_dttm)

        if to_dttm is not None:
            account_hist = session.query(AccountHist).filter(AccountHist.created_at <= to_dttm)

        if proc_div is not None:
            account_hist = session.query(AccountHist).filter(AccountHist.proc_div == proc_div)

        print("Repository 계층 아웃")
        return account_hist.limit(20).all()




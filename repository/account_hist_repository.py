from entity.account_hist import AccountHist

'''
account_hist 테이블에 저장
'''
class AccountHistRepository:

    def insert(self, session, account_hist: AccountHist):
        session.add(account_hist)
        session.commit()

#User.id >= 1, User.email == 'example@example.com'
    def search_by_dttm_and_job_div(self, customer_id, account_id, from_dttm, to_dttm, banking_div):

        # from_dttm, to_dttm이 정상적으로 포함했는지 확인 필요함
        # bankingdiv 도 마찬가지
        accounts = (AccountHist.query
                    .filter(AccountHist.account_id == account_id
                            , AccountHist.customer_id == customer_id
                            , AccountHist.created_at >= from_dttm
                            , AccountHist.created_at <= to_dttm
                            , AccountHist.banking_div == banking_div)
                    .limit(20)
                    .all()
                    )



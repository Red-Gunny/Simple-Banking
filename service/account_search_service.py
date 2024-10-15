from repository.account_base_repository import AccountBaseRepository
from repository.account_hist_repository import AccountHistRepository
from serial.request import banking_hist_request


class AccountSearchService:

    def __init__(self):
        self.account_base_repository = AccountBaseRepository()
        self.account_hist_repository = AccountHistRepository()

    ''' 계좌 유효성 검사 수행 메소드 '''
    def check_valid_account_by_customer_id(self, session, account_id, customer_id):
        accounts = self.account_base_repository.search_by_customer_Id(session, customer_id)
        if accounts is None:
            return False
        for account in accounts:
            if account.account_id == account_id:
                return True
        return False

    ''' 
    조회조건 1 : 거래일시
    조회조건 2 : 출금 / 입금
    from_dttm, to_dttm, banking_div
    '''
    def search_banking_hist_by_conditions(self, session, hist_request:banking_hist_request):

        print("service 계층 인입")

        print(hist_request.account_id)
        print(hist_request.customer_id)
        print(hist_request.search_from_dt)
        print(hist_request.search_to_dt)
        print(hist_request.filter_action)
        print(hist_request.request_time)

        result = self.account_hist_repository.search_by_dttm_and_job_div(
            session
            , customer_id = hist_request.customer_id
            , account_id = hist_request.account_id
            , from_dttm = hist_request.search_from_dt
            , to_dttm = hist_request.search_to_dt
            , banking_div = hist_request.filter_action
        )
        print(result)
        print("service 계층 아웃")
        return result









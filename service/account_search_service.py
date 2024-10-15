from repository.account_base_repository import AccountBaseRepository


class AccountSearchService:

    def __init__(self):
        self.account_base_repository = AccountBaseRepository()

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
    '''
    #def search_banking_hist_by_conditions(self, from_dttm, to_dttm, banking_div):










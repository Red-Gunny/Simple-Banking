from entity.account_hist import AccountHist
from repository.account_base_repository import AccountBaseRepository
from repository.account_hist_repository import AccountHistRepository
from datetime import datetime

from serial.response.withdraw_response import WithdrawResponse


class WithdrawService:

    def __init__(self):
        self.account_base_repository = AccountBaseRepository()
        self.account_hist_repository = AccountHistRepository()


    # (1) 기존 계좌 정보조회 - 계좌 잔고 확인
    # (2) 계좌 상태 변경
    # (3) 계좌 이력 저장
    def withdraw(self, session, request_obj, job_req_id):
        # (1) 기존 계좌 정보 조회
        last_account = self.account_hist_repository.search_last_account_history(session=session
                                                                                , account_id = request_obj.account_id)
        # 계좌 잔고 에러
        if last_account.balance < int(request_obj.amount):
            return False, "8899"

        # (2) 계좌 기본 수정
        self.account_base_repository.update_balance_and_last_proc_dttm(session=session
                                                                       , account_id = request_obj.account_id
                                                                       , amount= int(request_obj.amount) * -1)

        # (3) 계좌 이력 저장
        account_hist = self.convert_account_hist_entity(request_obj = request_obj
                                                        ,last_account = last_account)
        self.account_hist_repository.insert(session=session
                                            , account_hist=account_hist)

        return self.to_WithdrawResponse(request_obj=request_obj, is_success=True, job_req_id=job_req_id)

    '''
        ACCOUNT_HIST 엔티티 매핑
    '''
    def convert_account_hist_entity(self, request_obj, last_account):
        account_hist = AccountHist()
        account_hist.account_id = request_obj.account_id
        account_hist.seq = last_account.seq + 1

        account_hist.customer_id = request_obj.customer_id
        account_hist.proc_div = "0002"
        account_hist.proc_dttm = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        account_hist.amount = int(request_obj.amount)
        account_hist.balance = last_account.balance - int(request_obj.amount)

        account_hist.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        account_hist.modified_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return account_hist


    def to_WithdrawResponse(self, request_obj, is_success, job_req_id):
        response = WithdrawResponse(account_id = request_obj.account_id
                                    , customer_id = request_obj.customer_id
                                    , proc_id = job_req_id
                                    , stat_cd = "0000")
        if not is_success:
            response.stat_cd = "9999"
        return response


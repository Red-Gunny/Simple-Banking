from entity.account_hist import AccountHist
from repository.account_base_repository import AccountBaseRepository
from repository.account_hist_repository import AccountHistRepository
from datetime import datetime

from serial.response.deposit_response import DepositResponse



class DepositService:

    def __init__(self):
        self.account_base_repository = AccountBaseRepository()
        self.account_hist_repository = AccountHistRepository()

    # (1) 기존 계좌 정보 조회
    # (2) 계좌 상태 변경
    # (3) 계좌 이력 저장
    def deposit(self, session, request_obj, job_req_id):
        # (1) 기존 계좌 정보 조회
        last_account = self.account_hist_repository.search_last_account_history(session=session
                                                                                , account_id = request_obj.account_id)
        # (2) 계좌 기본 저장
        self.account_base_repository.update_balance_and_last_proc_dttm(session = session
                                                                       , account_id=request_obj.account_id
                                                                       , amount=int(request_obj.amount))
        # (3) 계좌 이력 저장
        account_hist = self.convert_account_hist_entity(request_obj, last_account)
        self.account_hist_repository.insert(session, account_hist)
        return self.to_DespositResponse(request_obj=request_obj, is_success=True, job_req_id=job_req_id)


    '''
        ACCOUNT_HIST 엔티티 매핑
    '''
    def convert_account_hist_entity(self, request_obj, last_account):
        account_hist = AccountHist()
        account_hist.account_id = request_obj.account_id
        account_hist.seq = last_account.seq + 1

        account_hist.customer_id = request_obj.customer_id
        account_hist.proc_div = "0001"  # 0001 - 입금
        account_hist.proc_dttm = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        account_hist.amount = int(request_obj.amount)
        account_hist.balance = last_account.balance + int(request_obj.amount)
        account_hist.etc = request_obj.etc

        account_hist.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        account_hist.modified_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return account_hist


    def to_DespositResponse(self, request_obj, is_success, job_req_id):
        response = DepositResponse(
            account_id=request_obj.account_id
            , customer_id=request_obj.customer_id
            , proc_id=job_req_id
            , stat_cd="0000"
        )
        if not is_success:
            response.stat_cd = "9999"
        return response


'''
deprecated code
'''
    # account_base = self.convert_account_base_entity(request_obj, job_req_id)
    # (1) 작업 이력 저장
    # '''
    #     JOB_HIST 엔티티 매핑
    # '''
    # def convert_job_hist_entity(self, request_obj, job_req_id):
    #     job_hist = JobHist()
    #     job_hist.job_id = job_req_id #str(uuid.uuid4()).replace("-", "")
    #     job_hist.customer_id = request_obj.user_id
    #     job_hist.account_id = request_obj.account_id
    #     job_hist.job_div = "0001"
    #     job_hist.proc_stat_cd = "0001"
    #     job_hist.amount = int(request_obj.amount)
    #     job_hist.request_dttm = request_obj.request_time
    #     now = datetime.now()
    #     formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    #     job_hist.created_at = formatted_time
    #     job_hist.modified_at = formatted_time
    #     return job_hist
    #
    # '''
    #     ACCOUNT_BASE 엔티티 매핑
    # '''
    # def convert_account_base_entity(self, request_obj, job_req_id):
    #     account_base = AccountBase()
    #     account_base.job_id = job_req_id   #str(uuid.uuid4()).replace("-", "")
    #     account_base.customer_id = request_obj.user_id
    #     account_base.account_id = request_obj.account_id
    #     account_base.job_div = "0001"
    #     account_base.proc_stat_cd = "0001"
    #     account_base.amount = int(request_obj.amount)
    #     account_base.request_dttm = request_obj.request_time
    #     now = datetime.now()
    #     formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    #     account_base.created_at = formatted_time
    #     account_base.modified_at = formatted_time
    #     return account_base

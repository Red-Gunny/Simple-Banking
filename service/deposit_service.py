from entity.account_base import AccountBase
from entity.account_hist import AccountHist
from entity.job_hist import JobHist
from repository.account_base_repository import AccountBaseRepository
from repository.account_hist_repository import AccountHistRepository
from repository.job_hist_repository import JobHistRepository
from datetime import datetime
import uuid

class DepositService:

    def __init__(self):
        self.job_hist_repository = JobHistRepository()
        self.account_base_repository = AccountBaseRepository()
        self.account_hist_repository = AccountHistRepository()


    # (1) 작업 이력 저장
    # (2) 계좌 상태 변경
    # (3) 계좌 이력 저장
    def deposit(self, session, request_obj):

        # (1) 작업 이력 저장
        job_hist = self.convert_job_hist_model(request_obj)
        self.job_hist_repository.insert(session, job_hist)

        # TODO 1 : update해야 함
        # (2) 계좌 기본 저장
        account_base = self.convert_account_base_entity(request_obj)
        self.account_base_repository.insert(session, account_base)

        # (3) 계좌 이력 저장
        account_hist = self.convert_account_hist_entity(request_obj)
        self.account_hist_repository.insert(session, account_hist)

        return True


    '''
        JOB_HIST 엔티티 매핑
    '''
    def convert_job_hist_entity(request_obj):
        job_hist = JobHist()
        job_hist.job_id = str(uuid.uuid4()).replace("-", "")
        job_hist.customer_id = request_obj.user_id
        job_hist.account_id = request_obj.account_id
        job_hist.job_div = "0001"
        job_hist.proc_stat_cd = "0001"
        job_hist.amount = int(request_obj.amount)
        job_hist.request_dttm = request_obj.request_time
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        job_hist.created_at = formatted_time
        job_hist.modified_at = formatted_time
        return job_hist

    '''
        ACCOUNT_BASE 엔티티 매핑
    '''
    def convert_account_base_entity(request_obj):
        account_base = AccountBase()
        account_base.job_id = str(uuid.uuid4()).replace("-", "")
        account_base.customer_id = request_obj.user_id
        account_base.account_id = request_obj.account_id
        account_base.job_div = "0001"
        account_base.proc_stat_cd = "0001"
        account_base.amount = int(request_obj.amount)
        account_base.request_dttm = request_obj.request_time
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        account_base.created_at = formatted_time
        account_base.modified_at = formatted_time
        return account_base

    '''
        ACCOUNT_HIST 엔티티 매핑
    '''
    def convert_account_hist_entity(request_obj):
        account_hist = AccountHist()
        account_hist.job_id = str(uuid.uuid4()).replace("-", "")
        account_hist.customer_id = request_obj.user_id
        account_hist.account_id = request_obj.account_id
        account_hist.job_div = "0001"
        account_hist.proc_stat_cd = "0001"
        account_hist.amount = int(request_obj.amount)
        account_hist.request_dttm = request_obj.request_time
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        account_hist.created_at = formatted_time
        account_hist.modified_at = formatted_time
        return account_hist





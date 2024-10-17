import uuid
from datetime import datetime

from entity.job_hist import JobHist
from repository.job_hist_repository import JobHistRepository


class JobHistControlService:

    def __init__(self):
        self.job_hist_repository = JobHistRepository()

    # 요청 시 최초 작업 기록
    def insert_ready_job(self, session, customer_id : str, account_id : str, amount : int, job_div : str):

        # JOB_HIST에 넣을 객체 생성
        job_hist = JobHist()
        job_hist.job_id = str(uuid.uuid4()).replace("-", "")
        job_hist.customer_id = customer_id
        job_hist.account_id = account_id
        job_hist.job_div = job_div               # "0001" : 입금 / "0002" : 출금
        job_hist.proc_stat_cd = "0001"          # "0001" : 대기 / "0002" : 완료  / "0003" : 실패
        job_hist.amount = amount
        job_hist.request_dttm = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        job_hist.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        job_hist.modified_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.job_hist_repository.insert(session = session, job_hist = job_hist)

        return job_hist, job_hist.job_id


    # 작업 실패 기록
    def update_fail_job(self, session, job_id):
        self.job_hist_repository.update_fail_by_job_id(session = session, job_id = job_id)

    # 작업 실패 기록
    def update_success_job(self, session, job_id):
        self.job_hist_repository.update_success_by_job_id(session=session, job_id=job_id)


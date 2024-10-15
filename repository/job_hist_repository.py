

'''
account_base 테이블에 저장
'''
from entity.job_hist import JobHist


class JobHistRepository:

    def insert(self, session, job_hist: JobHist):
        session.add(job_hist)
        session.commit()


from entity.account_base import JobHist

'''
account_base 테이블에 저장
'''
class JobHistRepository:


    def insert(session, job_hist: JobHist):
        session.add(job_hist)
        session.commit()


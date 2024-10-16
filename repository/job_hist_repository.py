from entity.job_hist import JobHist

'''
JOB_HIST 테이블에 저장
'''
class JobHistRepository:

    def insert(self, session, job_hist: JobHist):
        session.add(job_hist)
        session.commit()


    def update_fail_by_job_id(self, session, job_id):
        session.query(JobHist).filter(JobHist.job_id == job_id).update({JobHist.proc_stat_cd : "0003"})
        session.commit()

    def update_success_by_job_id(self, session, job_id):
        session.query(JobHist).filter(JobHist.job_id == job_id).update({JobHist.proc_stat_cd : "0002"})
        session.commit()

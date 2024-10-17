from sqlalchemy import text

def create_table(engine):
    create_job_hist_table(engine)
    create_account_base_table(engine)
    create_account_hist_table(engine)
    create_customer_table(engine)


'''
작업 이력 테이블
'''
def create_job_hist_table(engine):
    job_hist_query = '''CREATE TABLE job_hist (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        job_id VARCHAR(255) UNIQUE NOT NULL,
                                        customer_id VARCHAR(255) NOT NULL,
                                        account_id VARCHAR(255) NOT NULL,
                                        job_div VARCHAR(4) NOT NULL,
                                        proc_stat_cd VARCHAR(4) NOT NULL,
                                        amount VARCHAR(255) NOT NULL,
                                        request_dttm TIMESTAMP NOT NULL,
                                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                        modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                            );
                                        '''
    with engine.connect() as connection:
        connection.execute(text(job_hist_query))


'''
계좌 기본 원장 (로컬 테스트 목적)
'''
def create_account_base_table(engine):
    account_base_query = """CREATE TABLE IF NOT EXISTS account_base  (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  account_id VARCHAR(255) NOT NULL,
                                  customer_id VARCHAR(255) NOT NULL,
                                  balance NUMERIC(20, 0) NOT NULL,
                                  last_proc_dttm TIMESTAMP,
                                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                  modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                  UNIQUE (account_id)  
                                );
                            """
    with engine.connect() as connection:
        connection.execute(text(account_base_query))



'''
계좌 이력 원장 (로컬 테스트 목적)
'''
def create_account_hist_table(engine):
    account_hist_query = """
            CREATE TABLE IF NOT EXISTS  account_hist (
                                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                account_id VARCHAR(255) NOT NULL,
                                                seq BIGINT NOT NULL,
                                                customer_id VARCHAR(255) NOT NULL,
                                                proc_div VARCHAR(4) NOT NULL,
                                                proc_dttm TIMESTAMP NOT NULL,
                                                amount NUMERIC(20, 0) NOT NULL,
                                                balance NUMERIC(20, 0) NOT NULL,
                                                etc TEXT,
                                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                UNIQUE (account_id, seq)  
                                             );
                            """
    with engine.connect() as connection:
        connection.execute(text(account_hist_query))


'''
고객 원장
'''
def create_customer_table(engine):
    customer_base_query = """
                                CREATE TABLE customer_base (
                                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            customer_id VARCHAR(255) UNIQUE NOT NULL,
                                                            status VARCHAR(4) NOT NULL,
                                                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                            modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                                        );
                                """
    with engine.connect() as connection:
        connection.execute(text(customer_base_query))

from sqlalchemy import text
from test.table_definition import TableDefinition

def create_table(engine):
    create_job_hist_table(engine)
    create_account_base_table(engine)
    create_account_hist_table(engine)
    create_customer_table(engine)


'''
입금 출금 작업 요청 기록 테이블을 생성함 (테스트 목적 )
id : 자동 증가
'''
def create_job_hist_table(engine):

    job_hist = TableDefinition(
        "job_hist",
        {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "job_id": "VARCHAR(255) UNIQUE NOT NULL",
            "customer_id": "VARCHAR(255) NOT NULL",
            "account_id": "VARCHAR(255) NOT NULL",
            "job_div": "VARCHAR(4) NOT NULL",
            "proc_stat_cd": "VARCHAR(4) NOT NULL",
            "amount": "VARCHAR(255) NOT NULL",
            "request_dttm": "TIMESTAMP NOT NULL",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "modified_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        }
    )
    create_query = job_hist.create_table_query()
    with engine.connect() as connection:
        connection.execute(text(create_query))



'''
계좌 기본 원장 (로컬 테스트 목적)
'''
def create_account_base_table(engine):
    account_base = TableDefinition(
        "account_base",
        {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",      # Sqlite3 에서는 8바이트
            "account_id": "VARCHAR(255) UNIQUE NOT NULL",
            "status": "VARCHAR(4) NOT NULL",
            "customer_id": "VARCHAR(255) NOT NULL",
            "balance" : "NUMERIC(20, 0) NOT NULL",
            "etc": "TEXT",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "modified_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        }
    )
    create_query = account_base.create_table_query()
    with engine.connect() as connection:
        connection.execute(text(create_query))


'''
계좌 이력 원장 (로컬 테스트 목적)
'''
def create_account_hist_table(engine):
    account_hist = TableDefinition(
        "account_hist",
        {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "account_id": "VARCHAR(255) UNIQUE NOT NULL ",
            "seq": "BIGINT UNIQUE NOT NULL",
            "status": "VARCHAR(4) NOT NULL",
            "customer_id": "VARCHAR(255) NOT NULL",
            "balance": "NUMERIC(20, 0) NOT NULL",
            "etc": "TEXT",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "modified_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        }
    )
    create_query = account_hist.create_table_query()
    with engine.connect() as connection:
        connection.execute(text(create_query))

'''
고객 원장
'''
def create_customer_table(engine):
    customer_base = TableDefinition(
        "customer_base",
        {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "customer_id": "VARCHAR(255) UNIQUE NOT NULL",
            "status": "VARCHAR(4) NOT NULL",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "modified_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        }
    )
    create_query = customer_base.create_table_query()
    with engine.connect() as connection:
        connection.execute(text(create_query))
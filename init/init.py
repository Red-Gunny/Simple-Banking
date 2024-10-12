# SQLite 데이터베이스 경로
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, sessionmaker
from test.table_definition import TableDefinition

def init():
    conn = get_db_connection_by_sqlalchemy()


def get_db_connection_by_sqlalchemy():
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    return engine.raw_connection()


'''
입금 출금 작업 요청 기록 테이블을 생성함 (테스트 목적 )
id : 자동 증가
'''
def create_job_hist_table(conn):

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
    cursor = conn.cursor()
    create_query = job_hist.create_table_query()
    cursor.execute(create_query)
    conn.commit()



'''
계좌 기본 원장 (로컬 테스트 목적)
'''
def create_account_base_table(conn):
    acconut_base = TableDefinition(
        "acconut_base",
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
    cursor = conn.cursor()
    create_query = acconut_base.create_table_query()
    cursor.execute(create_query)
    conn.commit()


'''
계좌 이력 원장 (로컬 테스트 목적)
'''
def create_account_hist_table(conn):
    acconut_hist = TableDefinition(
        "acconut_hist",
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
    cursor = conn.cursor()
    create_query = acconut_hist.create_table_query()
    cursor.execute(create_query)
    conn.commit()

'''
고객 원장
'''
def create_customer_table(conn):
    acconut_hist = TableDefinition(
        "acconut_hist",
        {
            "id": "BIGINT PRIMARY KEY AUTOINCREMENT",
            "customer_id": "VARCHAR(255) UNIQUE NOT NULL",
            "status": "VARCHAR(4) NOT NULL",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "modified_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        }
    )
    cursor = conn.cursor()
    create_query = acconut_hist.create_table_query()
    cursor.execute(create_query)
    conn.commit()
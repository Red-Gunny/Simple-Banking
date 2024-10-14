from flask import Flask, request
from config import db_config
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from init.init import create_table
from request.deposit_request import DepositRequest
from service.deposit_service import DepositService
from pydantic import BaseModel, ValidationError

app = Flask(__name__)                  # Flask 어플리케이션 인스턴스를 생성한다.
app.config.from_object(db_config)      # 설정 객체를 로드해서 Flask 어플리케이션에 적용한다.

#Base = declarative_base()               # entity에 테이블을 매핑하기 위한 Base Entity
#Base.metadata.create_all(engine)

engine = create_engine('sqlite:///my_database.db', echo=True)     # DB 연결주소 / 실행 쿼리 표시
Session = sessionmaker(bind=engine)     # Session은 세션 팩토리
create_table(engine)
#conn = engine.raw_connection()



@app.route('/', methods=['GET'])
def hello():
    return "this is anking"


@app.route('/deposit', methods=['POST'])
def deposit():
    if request.json is None:
        return "error"
    session = Session()
    deposit_request = DepositRequest(**request.json)
    deposit_service = DepositService()
    result = deposit_service.deposit(session, deposit_request)
    if result :
        return "happy banking"
    else :
        return "unhappy"



from flask import Flask, request, jsonify
from config import db_config
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, sessionmaker
from init.init import init
from service.deposit_service import DepositService

app = Flask(__name__)                    # Flask 어플리케이션 인스턴스를 생성한다.
app.config.from_object(db_config)       # 설정 객체를 로드해서 Flask 어플리케이션에 적용한다.
engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
init()

#db.init_app(app)                           #SQLAlchemy를 초기화 한다.

#with app.app_context():                 # 어플리케이션 컨텍스트를 사용해서 DB 테이블을 생성한다. 테이블이 없는 경우에만 작동한다.
#    db.create_all()

@app.route('/', methods=['GET'])
def hello():
    return "this is anking"


@app.route('/', methods=['POST'])
def deposit():
    session = Session()
    depost_service = DepositService()
    result = depost_service.deposit(session, account_id="1", amount= "10000")
    if result :
        return "happy banking"
    else :
        return "unhappy"



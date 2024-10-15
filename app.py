from flask import Flask, request, jsonify
from config import db_config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from init.init import create_table
from serial.request.banking_hist_request import BankingHistRequest
from serial.request.deposit_request import DepositRequest
from serial.request.withdraw_request import WithdrawRequest
from serial.response.error_response import ErrorResponse
from service.account_search_service import AccountSearchService
from service.deposit_service import DepositService
from service.withdraw_service import WithdrawService

app = Flask(__name__)                  # Flask 어플리케이션 인스턴스를 생성한다.
app.config.from_object(db_config)      # 설정 객체를 로드해서 Flask 어플리케이션에 적용한다.
#db = SQLAlchemy(app)

engine = create_engine('sqlite:///my_database.db', echo=True)     # DB 연결주소 / 실행 쿼리 표시
Session = sessionmaker(bind=engine)     # Session은 세션 팩토리
create_table(engine)
#conn = engine.raw_connection()


''' 필요 객체 정의'''
account_search_service = AccountSearchService()

@app.route('/', methods=['GET'])
def hello():
    return "this is banking"


@app.route('/api/v1/<account_id>/transactions', methods=['GET'])
def get_transactions(account_id):
    if request.json is None:
        return "error"

    # 트랜잭션용 Session 객체 생성
    session = Session()

    # API 데이터 <-> 객체 변환
    hist_request = BankingHistRequest(**request.args.to_dict())
    hist_request.account_id = account_id
    if hist_request.request_dttm is None:
        hist_request.request_dttm = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 디버깅을 위해 쿼리 파라미터를 출력
    print(f"  account_id: {hist_request.account_id}"
          f", customer_id: {hist_request.customer_id}"
          f", search_from_dt: {hist_request.search_from_dt}"
          f", search_to_dt: {hist_request.search_to_dt}"
          f", filter_action: {hist_request.filter_action}"
          f", request_time: {hist_request.request_dttm}")

    # 계좌 유효성 검사
    is_valid = account_search_service.check_valid_account_by_customer_id( session=session
                                                                          , account_id=hist_request.account_id
                                                                          , customer_id=hist_request.customer_id)
    if not is_valid:
        error_response = ErrorResponse(
            account_id=hist_request.account_id
            , customer_id=hist_request.customer_id
            , error_cd=str(9999)
            , error_reason="고객 계좌번호 미보유"
        )
        return jsonify(error_response.model_dump())

    print("search_banking_hist_by_conditions 전 ")
    print(hist_request.account_id)
    print(hist_request.customer_id)
    print(hist_request.search_from_dt)
    print(hist_request.search_from_dt)
    banking_hist_response = account_search_service.search_banking_hist_by_conditions(session=session
                                                             , hist_request=hist_request)

    print("search_banking_hist_by_conditions 후 ")

    # 조회 코드 작성해야 함
    return jsonify(banking_hist_response.model_dump())


@app.route('/api/v1/deposit', methods=['POST'])
def deposit():
    if request.json is None:
        return "error"

    session = Session()
    deposit_request = DepositRequest(**request.json)

    # 계좌 유효성 검사

    is_valid = account_search_service.check_valid_account_by_customer_id(deposit_request.account_id)
    if not is_valid:
        return "error"

    # deposit 수행
    deposit_service = DepositService()
    result = deposit_service.deposit(session, deposit_request)
    if result:
        return "happy banking"
    else :
        return "unhappy"


@app.route('/api/v1/withdraw', methods=['POST'])
def withdraw():
    if request.json is None:
        return "error"
    session = Session()
    withdraw_request = WithdrawRequest(**request.json)

    # 계좌 유효성 검사
    account_search_service = AccountSearchService()
    is_valid = account_search_service.check_valid_account_by_customer_id(withdraw_request.account_id)
    if not is_valid:
        return "error"

    # 출금 수행
    withdraw_service = WithdrawService()
    result = withdraw_service.withdraw(session, withdraw_request)
    if result :
        return "happy banking"
    else :
        return "unhappy"



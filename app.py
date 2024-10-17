from flask import Flask, request, jsonify
from config import db_config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from init.init import create_table
from serial.request.banking_hist_request import BankingHistRequest
from serial.request.deposit_request import DepositRequest
from serial.request.withdraw_request import WithdrawRequest
from serial.response.error_response import ErrorResponse
from service.account_search_service import AccountSearchService
from service.deposit_service import DepositService
from service.job_hist_control_service import JobHistControlService
from service.withdraw_service import WithdrawService

app = Flask(__name__)                  # Flask 어플리케이션 인스턴스를 생성한다.
app.config.from_object(db_config)      # 설정 객체를 로드해서 Flask 어플리케이션에 적용한다.
engine = create_engine('sqlite:///my_database.db', echo=True)     # DB 연결주소 / 실행 쿼리 표시
Session = sessionmaker(bind=engine)     # Session은 세션 팩토리

''' 테스트용 DB 생성 (없을 때)'''
create_table(engine)

''' 필요 객체 정의'''
account_search_service = AccountSearchService()
deposit_service = DepositService()
withdraw_service = WithdrawService()
job_hist_control_service = JobHistControlService()


@app.route('/api/v1/<account_id>/transactions', methods=['GET'])
def get_transactions(account_id):
    if request.json is None:
        error_response = ErrorResponse(
            error_cd = str(9999)
            , error_reason = "JSON 객체 오류"
        )
        return jsonify(error_response.model_dump())

    # 트랜잭션용 Session 객체 생성
    session = Session()

    # API 데이터 <-> 객체 변환
    hist_request = BankingHistRequest(**request.args.to_dict())
    hist_request.account_id = account_id
    if hist_request.request_dttm is None:
        hist_request.request_dttm = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

    banking_hist_response = account_search_service.search_banking_hist_by_conditions(session=session
                                                                                    , hist_request=hist_request)

    # 조회 코드 작성해야 함
    return jsonify(banking_hist_response.model_dump())


@app.route('/api/v1/deposit', methods=['POST'])
def deposit():
    if request.json is None:
        error_response = ErrorResponse(
            error_cd=str(9999)
            , error_reason="JSON 객체 오류"
        )
        return jsonify(error_response.model_dump())

    # 트랜잭션 시작
    session = Session()

    # API 데이터 <-> 객체 변환
    deposit_request = DepositRequest(**request.json)

    # 작업 이력 테이블 내 요청 내용 기록
    job_hist, job_id = job_hist_control_service.insert_ready_job(session = session
                                                                 , customer_id = deposit_request.customer_id
                                                                 , account_id = deposit_request.account_id
                                                                 , amount = int(deposit_request.amount)
                                                                 , job_div = "0001")
    session.commit()

    # 계좌 유효성 검사
    is_valid = account_search_service.check_valid_account_by_customer_id(session= session
                                                                         , account_id = deposit_request.account_id
                                                                         , customer_id = deposit_request.customer_id)
    if not is_valid:
        # 작업 이력 테이블 내 작업 실패 기록
        job_hist_control_service.update_fail_job(session=session, job_id=job_id)
        # 작업 실패 응답 반환
        error_response = ErrorResponse(account_id=deposit_request.account_id
                                        , customer_id=deposit_request.customer_id
                                        , error_cd=str(4444)
                                        , error_reason="고객 계좌번호 미보유")
        return jsonify(error_response.model_dump())

    # 입금 수행
    deposit_response = deposit_service.deposit(session = session, request_obj=deposit_request, job_req_id= job_id)

    # 작업 이력 테이블 내 작업 성공 기록
    job_hist_control_service.update_success_job(session = session, job_id=job_id)
    session.commit()

    return jsonify(deposit_response.model_dump())


@app.route('/api/v1/withdraw', methods=['POST'])
def withdraw():
    if request.json is None:
        error_response = ErrorResponse(
            error_cd=str(9999)
            , error_reason="JSON 객체 오류"
        )
        return jsonify(error_response.model_dump())

    # 트랜잭션 시작
    session = Session()

    # API 데이터 <-> 객체 변환
    withdraw_request = WithdrawRequest(**request.json)

    # 작업 이력 테이블 내 요청 내용 기록
    job_hist, job_id = job_hist_control_service.insert_ready_job(session=session
                                                                 , customer_id=withdraw_request.customer_id
                                                                 , account_id=withdraw_request.account_id
                                                                 , amount=int(withdraw_request.amount)
                                                                 , job_div = "0002")

    # 계좌 유효성 검사
    is_valid = account_search_service.check_valid_account_by_customer_id(session= session
                                                                         , account_id = withdraw_request.account_id
                                                                         , customer_id = withdraw_request.customer_id)
    # 예외 처리 - 고객 계좌 매핑 오류
    if not is_valid:
        # 작업 이력 테이블 내 작업 실패 기록
        job_hist_control_service.update_fail_job(session=session, job_id=job_id)
        # 작업 실패 응답 반환
        error_response = ErrorResponse(account_id=withdraw_request.account_id
                                        , customer_id=withdraw_request.customer_id
                                        , error_cd=str(9999)
                                        , error_reason="고객 계좌번호 미보유")
        return jsonify(error_response.model_dump())

    # 출금 수행
    wtihdraw_response = withdraw_service.withdraw(session=session, request_obj = withdraw_request, job_req_id=job_id)

    # 작업 이력 테이블 내 작업 성공 기록
    job_hist_control_service.update_success_job(session=session, job_id=job_id)
    session.commit()

    return jsonify(wtihdraw_response.model_dump())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=40000)



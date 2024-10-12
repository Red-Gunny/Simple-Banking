from entity.account_base import AccountBase
from repository.account_base_repository import AccountBaseRepository


class DepositService:


    # (1) 작업 이력 저장
    # (2) 계좌 상태 변경
    # (3) 계좌 이력 저장
    def deposit(session, account_id: str, amount: str):
        amount = int(amount)
        # (1) 작업 이력 저장
        account_base = AccountBase(
            account_id="1"
            , status="0000"
            , customer_id = "aa"
            , balance= amount
            , etc = "적요"
            , created_at= "yyyy-MM-dd"
            , modified_at = "yyyy-MM-dd"
        )
        account_base_repository = AccountBaseRepository()
        account_base_repository.insert(session, account_base)

        # (2) 작업 이력 저장

        # (3) 계좌 이력 저장

        return True
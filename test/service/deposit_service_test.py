import unittest
from unittest.mock import MagicMock

from service.deposit_service import DepositService


class TestDepositService(unittest.TestCase):

    def setUp(self):
        self.deposit_service = DepositService()
        self.session = MagicMock()
        self.request_obj = MagicMock()
        self.job_req_id = "job_req_123"

        self.last_account = MagicMock()
        self.last_account.seq = 1
        self.last_account.balance = 5000

    def test_deposit_success(self):
        # 함수 목킹
        self.deposit_service.account_hist_repository.search_last_account_history = MagicMock(return_value=self.last_account)
        self.deposit_service.account_base_repository.update_balance_and_last_proc_dttm = MagicMock()
        self.deposit_service.account_hist_repository.insert = MagicMock()

        # Arrange
        self.request_obj.account_id = "123"
        self.request_obj.customer_id = "hong"
        self.request_obj.amount = 20000
        self.request_obj.etc = "etc"

        # Act
        response = self.deposit_service.deposit(self.session, self.request_obj, self.job_req_id)
        self.deposit_service.account_hist_repository.search_last_account_history.assert_called_once_with(
            session=self.session, account_id=self.request_obj.account_id
        )
        self.deposit_service.account_base_repository.update_balance_and_last_proc_dttm.assert_called_once_with(
            session=self.session, account_id=self.request_obj.account_id, amount=2000
        )
        self.deposit_service.account_hist_repository.insert.assert_called_once()

        #  assert
        self.assertEqual(response.account_id, self.request_obj.account_id)
        self.assertEqual(response.customer_id, self.request_obj.customer_id)
        self.assertEqual(response.proc_id, self.job_req_id)
        self.assertEqual(response.stat_cd, "0000")  # Success


if __name__ == "__main__":
    unittest.main()

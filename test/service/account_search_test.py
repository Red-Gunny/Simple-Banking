import unittest
from unittest.mock import MagicMock

from service.account_search_service import AccountSearchService


class TestAccountSearchService(unittest.TestCase):

    def setUp(self):
        self.service = AccountSearchService()
        self.service.account_base_repository = MagicMock()

    def test_check_valid_account_by_customer_id_with_no_accounts(self):
        # Arrange - search_by_customer_Id가 None을 반환하도록 설정
        self.service.account_base_repository.search_by_customer_Id.return_value = None

        # Act - account_id와 customer_id로 함수를 호출
        result = self.service.check_valid_account_by_customer_id(None, "123", "hong")

        # Assert - 결과가 False여야 함
        self.assertFalse(result)

    def test_check_valid_account_by_customer_id_with_valid_account(self):
        # Arrange -  search_by_customer_Id가 계좌 목록을 반환하도록 설정
        mock_accounts = [
            MagicMock(account_id="123"),
        ]
        self.service.account_base_repository.search_by_customer_Id.return_value = mock_accounts

        # Act - account_id가 일치하는 경우
        result = self.service.check_valid_account_by_customer_id(None, "123", "hong")

        # Assert - 결과가 True여야 함
        self.assertTrue(result)

    def test_check_valid_account_by_customer_id_with_invalid_account(self):
        # Arrange -  earch_by_customer_Id가 계좌 목록을 반환하지만 account_id는 일치하지 않음
        mock_accounts = [
            MagicMock(account_id='11111'),
            MagicMock(account_id='22222'),
        ]
        self.service.account_base_repository.search_by_customer_Id.return_value = mock_accounts

        # Act - account_id가 일치하지 않는 경우
        result = self.service.check_valid_account_by_customer_id(None, "123", "hong")

        # Assert - 결과가 False여야 함
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()

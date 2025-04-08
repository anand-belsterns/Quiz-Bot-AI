import unittest
from unittest.mock import MagicMock, patch
from userdetails import UserInfo

class TestUserInfo(unittest.TestCase):
    @patch('db.Database')
    def setUp(self, MockDatabase):
        self.user_info = UserInfo()
        self.user_info.db = MockDatabase.return_value

    def test_store_user_data_success(self):
        self.user_info.store_user_data('John Doe', 'john@example.com')
        self.user_info.db.insert_user.assert_called_once_with('John Doe', 'john@example.com')

    def test_store_user_data_empty_name(self):
        with patch('tkinter.messagebox.showwarning') as mock_warning:
            result = self.user_info.store_user_data('', 'john@example.com')
            mock_warning.assert_called_once_with('Warning', 'Please fill in all fields!')
            self.assertFalse(result)

    def test_store_user_data_empty_email(self):
        with patch('tkinter.messagebox.showwarning') as mock_warning:
            result = self.user_info.store_user_data('John Doe', '')
            mock_warning.assert_called_once_with('Warning', 'Please fill in all fields!')
            self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
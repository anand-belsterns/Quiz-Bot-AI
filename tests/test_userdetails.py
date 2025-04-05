import unittest
from userdetails import UserDetails

class TestUserDetails(unittest.TestCase):
    def setUp(self):
        self.user = UserDetails(name='John Doe', age=30)

    def test_get_name(self):
        self.assertEqual(self.user.get_name(), 'John Doe')

    def test_get_age(self):
        self.assertEqual(self.user.get_age(), 30)

    def test_set_name(self):
        self.user.set_name('Jane Doe')
        self.assertEqual(self.user.get_name(), 'Jane Doe')

    def test_set_age(self):
        self.user.set_age(25)
        self.assertEqual(self.user.get_age(), 25)

if __name__ == '__main__':
    unittest.main()
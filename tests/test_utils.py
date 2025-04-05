import unittest
from utils import some_function

class TestUtils(unittest.TestCase):
    def test_some_function(self):
        self.assertEqual(some_function(1, 2), 3)
        self.assertEqual(some_function(-1, 1), 0)

if __name__ == '__main__':
    unittest.main()
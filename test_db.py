import unittest
from db import your_function

class TestYourFunction(unittest.TestCase):
    def test_case_1(self):
        self.assertEqual(your_function(args), expected_result)

    def test_case_2(self):
        self.assertRaises(ExpectedException, your_function, args)

if __name__ == '__main__':
    unittest.main()
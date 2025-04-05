import unittest
from quiz import function_to_test

class TestQuiz(unittest.TestCase):
    def test_case_1(self):
        self.assertEqual(function_to_test(args), expected_result)

    def test_case_2(self):
        self.assertTrue(function_to_test(args))

if __name__ == '__main__':
    unittest.main()
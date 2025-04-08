import json
import unittest
from unittest.mock import mock_open, patch
from utils import load_questions

class TestLoadQuestions(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='[{
    "question": "What is the capital of France?",
    "answer": "Paris"
}]')
    def test_load_questions(self, mock_file):
        expected = [{"question": "What is the capital of France?", "answer": "Paris"}]
        result = load_questions()
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with('questions.json', 'r')

if __name__ == '__main__':
    unittest.main()
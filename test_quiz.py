import unittest
from unittest.mock import MagicMock, patch
from quiz import QuizApp
import tkinter as tk

class TestQuizApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = QuizApp(self.root)

    def test_create_user_info_page(self):
        self.app.create_user_info_page()
        self.assertIsNotNone(self.app.name_entry)
        self.assertIsNotNone(self.app.email_entry)

    @patch('quiz.Database')
    @patch('quiz.UserInfo')
    def test_create_quiz_selection_page(self, MockUserInfo, MockDatabase):
        self.app.name_entry.insert(0, 'Test User')
        self.app.email_entry.insert(0, 'test@example.com')
        self.app.create_quiz_selection_page()
        self.assertEqual(self.app.user_info.name, 'Test User')
        self.assertEqual(self.app.user_info.email, 'test@example.com')

    @patch('quiz.os.path.exists', return_value=True)
    @patch('quiz.json.load')
    def test_load_questions(self, mock_json_load, mock_exists):
        mock_json_load.return_value = [{'question': 'What is 2+2?', 'options': ['3', '4', '5', '6'], 'answer': 1}]
        self.app.selected_topic = 'Math'
        self.app.selected_difficulty = 'Easy'
        questions = self.app.load_questions()
        self.assertEqual(len(questions), 1)

    def test_get_topics(self):
        with patch('quiz.os.path.exists', return_value=True), 
             patch('quiz.os.listdir', return_value=['Math', 'Science']):
            topics = self.app.get_topics()
            self.assertEqual(topics, ['Math', 'Science'])

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
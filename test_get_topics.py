import os
import unittest
from unittest.mock import patch, MagicMock
from get_topics import get_topics

class TestGetTopics(unittest.TestCase):

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('tkinter.messagebox.showerror')
    def test_topics_folder_not_found(self, mock_showerror, mock_isdir, mock_listdir, mock_exists):
        mock_exists.return_value = False
        result = get_topics(None)
        mock_showerror.assert_called_once_with('Error', 'Topics folder not found: ' + os.path.join(os.path.dirname(__file__), 'topic'))
        self.assertEqual(result, [])

    @patch('os.path.exists')
    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_get_topics_success(self, mock_isdir, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ['topic1', 'topic2', 'not_a_directory']
        mock_isdir.side_effect = lambda x: x in [os.path.join(os.path.dirname(__file__), 'topic', 'topic1'), os.path.join(os.path.dirname(__file__), 'topic', 'topic2')]
        result = get_topics(None)
        self.assertEqual(result, ['topic1', 'topic2'])

if __name__ == '__main__':
    unittest.main()
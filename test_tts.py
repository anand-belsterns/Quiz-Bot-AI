import unittest
from unittest.mock import patch, MagicMock
from tts import speak_text

class TestSpeakText(unittest.TestCase):
    @patch('pyttsx3.init')
    def test_speak_text_with_female_voice(self, mock_init):
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine
        mock_engine.getProperty.return_value = [MagicMock(name='Voice', id='1', name='Female Voice 1'), 
                                                MagicMock(name='Voice', id='2', name='Female Voice 2')]
        speak_text('Hello, world!')
        mock_engine.setProperty.assert_called_with('voice', '2')
        mock_engine.say.assert_called_with('Hello, world!')
        mock_engine.runAndWait.assert_called_once()

    @patch('pyttsx3.init')
    def test_speak_text_with_no_female_voice(self, mock_init):
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine
        mock_engine.getProperty.return_value = [MagicMock(name='Voice', id='1', name='Male Voice 1')]
        speak_text('Hello, world!')
        mock_engine.setProperty.assert_called_with('voice', '1')
        mock_engine.say.assert_called_with('Hello, world!')
        mock_engine.runAndWait.assert_called_once()

if __name__ == '__main__':
    unittest.main()
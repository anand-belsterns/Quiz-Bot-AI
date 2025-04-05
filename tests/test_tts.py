import unittest
from tts import TextToSpeech

class TestTextToSpeech(unittest.TestCase):
    def setUp(self):
        self.tts = TextToSpeech()

    def test_synthesize_speech(self):
        result = self.tts.synthesize('Hello World')
        self.assertIsNotNone(result)
        self.assertIsInstance(result, bytes)

    def test_set_language(self):
        self.tts.set_language('en')
        self.assertEqual(self.tts.language, 'en')

    def test_invalid_language(self):
        with self.assertRaises(ValueError):
            self.tts.set_language('invalid')

if __name__ == '__main__':
    unittest.main()
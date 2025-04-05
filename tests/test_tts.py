import unittest
from tts import TextToSpeech

class TestTextToSpeech(unittest.TestCase):
    def setUp(self):
        self.tts = TextToSpeech()

    def test_synthesize_speech(self):
        result = self.tts.synthesize_speech('Hello, world!')
        self.assertIsNotNone(result)

    def test_set_language(self):
        self.tts.set_language('en')
        self.assertEqual(self.tts.language, 'en')

if __name__ == '__main__':
    unittest.main()
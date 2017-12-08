import unittest

from libs.google_actions import AppResponse


class TestResponse(unittest.TestCase):
    def test_ask_fundamentals(self):
        result = AppResponse().ask('hello', 'TEST_CONVERSATION_TOKEN')
        self.assertTrue(result['expectUserResponse'])
        self.assertEqual(result['conversationToken'], 'TEST_CONVERSATION_TOKEN')
        self.assertIn(
            {'simpleResponse': {'textToSpeech': 'hello'}},
            result['expectedInputs']['inputPrompt']['richInitialPrompt']['items'])

    def test_tell_fundamentals(self):
        result = AppResponse().tell('bye', 'TEST_CONVERSATION_TOKEN')
        self.assertFalse(result['expectUserResponse'])
        self.assertEqual(result['conversationToken'], 'TEST_CONVERSATION_TOKEN')
        self.assertIn(
            {'simpleResponse': {'textToSpeech': 'bye'}},
            result['finalResponse']['richResponse']['items'])

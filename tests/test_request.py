import unittest

from libs.google_actions import AppRequest, NoJsonException
from .mocks import MockRequest


class TestRequest(unittest.TestCase):
    def test_parsing_fundamentals(self):
        body = """{"user":{"userId":"TEST_USER_ID","locale":"en-US","lastSeen":"2017-12-03T21:20:57Z"},"conversation":{"conversationId":"1512372865111","conversationToken":"TOKEN","type":"NEW"},"inputs":[{"intent":"actions.intent.TEXT","rawInputs":[{"inputType":"KEYBOARD","query":"hello"}],"arguments":[{"name":"text","rawText":"hello","textValue":"hello"}]}],"surface":{"capabilities":[{"name":"actions.capability.AUDIO_OUTPUT"},{"name":"actions.capability.SCREEN_OUTPUT"}]},"isInSandbox":true,"availableSurfaces":[{"capabilities":[{"name":"actions.capability.AUDIO_OUTPUT"},{"name":"actions.capability.SCREEN_OUTPUT"}]}]}"""  # noqa

        request = AppRequest(MockRequest(body=body))
        self.assertEqual(request.text, 'hello')
        self.assertEqual(request.user_id, 'TEST_USER_ID')
        self.assertEqual(request.conversation_id, '1512372865111')
        self.assertEqual(request.conversation_token, 'TOKEN')
        self.assertFalse(request.is_health_check)

    def test_raises_no_json_exception(self):
        with self.assertRaises(NoJsonException):
            AppRequest(MockRequest(body='NOT JSON'))

    def test_text_none_if_no_arguments(self):
        body = """{"user":{"userId":"USER_ID","locale":"en-US","lastSeen":"2017-12-02T18:55:46Z"},"conversation":{"conversationId":"1512240961019","type":"NEW"},"inputs":[{"intent":"actions.intent.MAIN","rawInputs":[{"inputType":"KEYBOARD","query":"Talk to Digger Sam"}]}],"surface":{"capabilities":[{"name":"actions.capability.AUDIO_OUTPUT"},{"name":"actions.capability.SCREEN_OUTPUT"}]},"isInSandbox":true,"availableSurfaces":[{"capabilities":[{"name":"actions.capability.AUDIO_OUTPUT"},{"name":"actions.capability.SCREEN_OUTPUT"}]}]}"""  # noqa
        result = AppRequest(MockRequest(body=body))
        self.assertEqual(result.text, None)

    def test_if_no_text_value(self):
        body = """{"user":{"userId":"TEST_USER_ID","locale":"en-US","lastSeen":"2017-12-03T21:20:57Z"},"conversation":{"conversationId":"1512372865111","conversationToken":"TOKEN","type":"NEW"},"inputs":[{"intent":"actions.intent.TEXT","rawInputs":[{"inputType":"KEYBOARD","query":"hello"}],"arguments":[{"name":"text","rawText":"hello"}]}],"surface":{"capabilities":[{"name":"actions.capability.AUDIO_OUTPUT"},{"name":"actions.capability.SCREEN_OUTPUT"}]},"isInSandbox":true,"availableSurfaces":[{"capabilities":[{"name":"actions.capability.AUDIO_OUTPUT"},{"name":"actions.capability.SCREEN_OUTPUT"}]}]}"""  # noqa
        request = AppRequest(MockRequest(body=body))
        self.assertEqual(request.text, 'hello')

    def test_health_check_detection(self):
        body = """{"user":{"userId":"TEST_USER_ID","profile":{"givenName":"Google","familyName":"Crawler"},"locale":"en-US"},"conversation":{"conversationId":"1524087953854","type":"NEW"},"inputs":[{"intent":"actions.intent.MAIN","rawInputs":[{"inputType":"VOICE","query":"true sight"}],"arguments":[{"name":"is_health_check","boolValue":true,"textValue":"1"}]}],"surface":{"capabilities":[{"name":"actions.capability.AUDIO_OUTPUT"}]}}""" # noqa
        request = AppRequest(MockRequest(body=body))
        self.assertTrue(request.is_health_check)

    def test_structured_inputs(self):
        body = """{"user":{"userId":"1234567890123","locale":"en-US"},"conversation":{"conversationId":"1524088228071","type":"NEW"},"inputs":[{"intent":"actions.intent.MAIN","rawInputs":[{"inputType":"VOICE","query":"what are some games that I can play right now"}],"arguments":[{"name":"game","structuredValue":{"description":"are","@context":"https://schema.org","@type":"Game"}},{"name":"trigger_query","rawText":"what are some games that I can play right now","textValue":"what are some games that I can play right now"}]}],"surface":{"capabilities":[{"name":"actions.capability.MEDIA_RESPONSE_AUDIO"},{"name":"actions.capability.AUDIO_OUTPUT"}]}}""" # noqa
        request = AppRequest(MockRequest(body=body))
        self.assertEqual(request.text, "what are some games that I can play right now")

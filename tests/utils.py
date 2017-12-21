import json


class Utils(object):
    @staticmethod
    def get_text_from_google_response(response):
        """Returns the text from within a response genearated with ask or tell.
        Useful for writing tests.
        """
        j = json.loads(response.content.decode('utf-8'))
        if 'expectedInputs' in j:  # ask
            response = j['expectedInputs']['inputPrompt']['richInitialPrompt']
        else:  # tell
            response = j['finalResponse']['richResponse']
        return response['items'][0]['simpleResponse']['textToSpeech']

    @staticmethod
    def get_conversation_token_from_google_response(response):
        j = json.loads(response.content.decode('utf-8'))
        return j['conversationToken']

    @classmethod
    def google_response_is_ask(cls, response):
        j = json.loads(response.content.decode('utf-8'))
        return (j['expectUserResponse'] is True
                and 'expectedInputs' in j
                and 'finalResponse' not in j)

    @staticmethod
    def google_response_is_tell(response):
        j = json.loads(response.content.decode('utf-8'))
        return (j['expectUserResponse'] is False
                and 'expectedInputs' not in j
                and 'finalResponse' in j)

import json


class Util(object):
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

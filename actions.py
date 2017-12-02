import logging

from django.http import JsonResponse


logger = logging.getLogger('django')


def ask(text):
    logger.debug("Asking {}".format(text))
    return JsonResponse(
        {
            "expectUserResponse": True,
            "isInSandbox": True,
            "expectedInputs": {
                "inputPrompt": {
                    "richInitialPrompt": {
                        "items": [
                            {
                                "simpleResponse": {
                                    "textToSpeech": text,
                                }
                            }
                        ]
                    }
                },
                "possibleIntents": [
                    {
                        'intent': "actions.intent.TEXT",
                    }
                ],
            }
        }
    )


def tell(text):
    """Ends the conversation"""
    logger.debug("Telling {}".format(text))
    return JsonResponse(
        {
            "expectUserResponse": False,
            "isInSandbox": True,
            "finalResponse": {
                "richResponse": {
                    "items": [
                        {
                            "simpleResponse": {
                                "textToSpeech": text,
                            }
                        }
                    ]
                }
            },
        }
    )

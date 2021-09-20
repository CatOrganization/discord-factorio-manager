import logging

import azure.functions as func

from DiscordWebhook.handlers import (BadRequest, application_command_handler,
                                     partial_http_request_handler,
                                     ping_handler,
                                     verify_request_signature_handler)

CLIENT_PUBLIC_KEY = '2ec6232217f7b9c05cf478d51678a5521e6696276308a23c26df928a23c3c505'

@partial_http_request_handler(verify_request_signature_handler(CLIENT_PUBLIC_KEY))
@partial_http_request_handler(ping_handler)
@partial_http_request_handler(application_command_handler)
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.warn('Function was not handled by middleware.')
    return BadRequest('Bad request')

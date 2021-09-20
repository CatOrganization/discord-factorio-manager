import json
import logging
import random
from typing import Iterable, Mapping, Optional, Union

import azure.functions as func

from discord_interactions import InteractionResponseType, InteractionType, verify_key

CLIENT_PUBLIC_KEY = '2ec6232217f7b9c05cf478d51678a5521e6696276308a23c26df928a23c3c505'

def Ok(body: Union[str, Mapping]) -> func.HttpResponse:
    if isinstance(body, Mapping):
        # convert to json
        body = json.dumps(body)

    return func.HttpResponse(body=body, status_code=200, mimetype='application/json')

def BadRequest(body: str) -> func.HttpResponse:
    return func.HttpResponse(body=body, status_code=401)



def status() -> func.HttpResponse:
    return Ok({
        'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        'data': {
            'content': 'status'
        }
    })

def start() -> func.HttpResponse:
    return Ok({
        'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        'data': {
            'content': 'start'
        }
    })

def stop() -> func.HttpResponse:
    return Ok({
        'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        'data': {
            'content': 'stop'
        }
    })


subcommand_to_handler = {
    'status': status,
    'start': start,
    'stop': stop,
}


def handle_application_command(json: Mapping) -> func.HttpResponse:
    command_name = json.get('data').get('name')
    logging.info('Processing application command %s', command_name)
    if command_name == 'factorio':
        options: Optional[Iterable[Mapping]] = json.get('data').get('options')
        logging.debug('There are %d option(s)', len(options))
        if len(options) == 1:
            option = options[0]
            option_type = option.get('type')
            logging.debug('Option type: %d', option_type)
            if option_type == 1:
                # option is a subcommand
                subcommand_name = option.get('name')
                logging.debug('Subcommand name: %s', subcommand_name)
                handler = subcommand_to_handler.get(subcommand_name)
                if handler is not None:
                    return handler()


    logging.warn('Unknown command %s', command_name)
    return BadRequest('Unknown command name')


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # TODO(asasine): make a function wrapper for key verification
    # TODO(asasine): make a function wrapper for ping requests
    signature = req.headers.get('X-Signature-Ed25519')
    timestamp = req.headers.get('X-Signature-Timestamp')
    if signature is None or timestamp is None:
        return BadRequest('Bad request signature')
        
    try:
        body: bytes = req.get_body()
    except ValueError:
        return BadRequest('Bad request signature')

    if not verify_key(body, signature, timestamp, CLIENT_PUBLIC_KEY):
        return BadRequest('Bad request signature')

    # if it's a PING request, respond immediately
    try:
        body_json: Mapping = req.get_json()
    except ValueError:
        return BadRequest('Bad request signature')

    request_type = body_json.get('type')
    if request_type == InteractionType.PING:
        logging.info('Got a PING')
        return Ok({
            'type': InteractionResponseType.PONG
        })
    elif request_type == InteractionType.APPLICATION_COMMAND:
        return handle_application_command(body_json)
    else:
        return BadRequest('Unknown request type: %d', request_type)

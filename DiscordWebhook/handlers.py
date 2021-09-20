import functools
import json
import logging
from typing import Callable, Iterable, Mapping, Optional, Union

import azure.functions as func
from discord_interactions import (InteractionResponseType, InteractionType,
                                  verify_key)

from DiscordWebhook.models import CommandOptionType


def Ok(body: Union[str, Mapping]) -> func.HttpResponse:
    if isinstance(body, Mapping):
        # convert to json
        body = json.dumps(body)

    return func.HttpResponse(body=body, status_code=200, mimetype='application/json')

    
def BadRequest(body: str) -> func.HttpResponse:
    return func.HttpResponse(body=body, status_code=400)


def Unauthorized(body: str) -> func.HttpResponse:
    return func.HttpResponse(body=body, status_code=401)
    

def partial_http_request_handler(handler: Callable[[func.HttpRequest], Optional[func.HttpResponse]]) -> Callable[[func.HttpRequest], func.HttpResponse]:
    """
    Creates a decorator from an HttpRequest handler.
    
    The handler returns None to indicate the request should be forwarded to the next handler.
    
    Args:
        handler:
            A callable which accepts an HttpRequest and returns an HttpResponse or None.
            If the returned value is None, the request is forwarded to the next handler.
            Otherwise, the pipeline is terminated and the returned value is the final return value.

    Returns:
        A decorator.
        The decorator wraps a function which accepts an HttpRequest and returns an HttpResponse
    """
    def decorator(f: Callable[[func.HttpRequest], func.HttpResponse]):
        @functools.wraps(f)
        def inner_decorator(req: func.HttpRequest) -> func.HttpResponse:
            response = handler(req)
            if response is not None:
                # handler handled the request
                return response
            else:
                # handler did not handle the request
                return f(req)
        return inner_decorator
    return decorator


def verify_request_signature_handler(client_public_key: str) -> Callable[[func.HttpRequest], Optional[func.HttpResponse]]:
    def inner(req: func.HttpRequest) -> Optional[func.HttpResponse]:
        logging.debug('Verifying request signature')
        signature = req.headers.get('X-Signature-Ed25519')
        timestamp = req.headers.get('X-Signature-Timestamp')
        if signature is None or timestamp is None:
            return Unauthorized('Bad request signature')
            
        try:
            body: bytes = req.get_body()
        except ValueError:
            return Unauthorized('Bad request signature')

        if not verify_key(body, signature, timestamp, client_public_key):
            return Unauthorized('Bad request signature')

        return None

    return inner


def ping_handler(req: func.HttpRequest) -> Optional[func.HttpResponse]:
    try:
        body_json: Mapping = req.get_json()
    except ValueError:
        # unable to handle this request without JSON data
        return None

    request_type = body_json.get('type')
    if request_type == InteractionType.PING:
        logging.info('Got a PING')
        return Ok({
            'type': InteractionResponseType.PONG
        })

    return None


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


def application_command_handler(req: func.HttpRequest) -> Optional[func.HttpResponse]:
    try:
        json: Mapping = req.get_json()
    except ValueError:
        # unable to handle this request without JSON data
        logging.debug('Unable to get JSON data')
        return None

    
    request_type = json.get('type')
    if request_type != InteractionType.APPLICATION_COMMAND:
        logging.debug(f'Request type {request_type} is not {InteractionType.APPLICATION_COMMAND}')
        return None

    command_name = json.get('data').get('name')
    logging.info('Processing application command: %s', command_name)
    if command_name == 'factorio':
        options: Optional[Iterable[Mapping]] = json.get('data').get('options')
        logging.debug('There are %d option(s)', len(options) if options is not None else 0)
        if options is not None and len(options) == 1:
            option = options[0]
            option_type = option.get('type')
            logging.debug('Option type: %d', option_type)
            if option_type == CommandOptionType.SUB_COMMAND:
                # option is a subcommand
                subcommand_name = option.get('name')
                logging.debug('Subcommand name: %s', subcommand_name)
                handler = subcommand_to_handler.get(subcommand_name)
                if handler is not None:
                    return handler()


    logging.warn('Unknown command: %s', command_name)
    return None

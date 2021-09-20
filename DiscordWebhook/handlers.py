
import json
from typing import Mapping, Union

import azure.functions as func
from discord_interactions import InteractionResponseType


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

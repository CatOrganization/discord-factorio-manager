import json
import logging
from typing import Mapping, Union

import azure.functions as func

from discord_interactions import InteractionResponseType, InteractionType, verify_key

CLIENT_PUBLIC_KEY = '2ec6232217f7b9c05cf478d51678a5521e6696276308a23c26df928a23c3c505'

def Ok(body: Union[str, Mapping]) -> func.HttpResponse:
    if isinstance(body, Mapping):
        # convert to json
        body = json.dumps(body)

    return func.HttpResponse(body=body, status_code=200)

def BadRequest(body: str) -> func.HttpResponse:
    return func.HttpResponse(body=body, status_code=401)



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

    if body_json.get('type') == InteractionType.PING:
        logging.info('Got a PING')
        return Ok({
            'type': InteractionResponseType.PONG
        })

    return Ok("hello discord")

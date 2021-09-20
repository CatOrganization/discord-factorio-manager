import json
from typing import Mapping, Union

import azure.functions as func


def Ok(body: Union[str, Mapping]) -> func.HttpResponse:
    if isinstance(body, Mapping):
        # convert to json
        body = json.dumps(body)

    return func.HttpResponse(body=body, status_code=200, mimetype='application/json')

    
def BadRequest(body: str) -> func.HttpResponse:
    return func.HttpResponse(body=body, status_code=400)


def Unauthorized(body: str) -> func.HttpResponse:
    return func.HttpResponse(body=body, status_code=401)
    
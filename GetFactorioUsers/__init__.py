import json
import logging
import os
import re

import azure.functions as func
import factorio_rcon as rcon

from DiscordWebhook.responses import Ok, BadRequest

PATTERN = r"\n  (?P<username>[a-zA-Z0-9_]+) \(online\)"


def get_factorio_rcon_password() -> str:
    return os.environ["FACTORIO_RCON_PASSWORD"]


def main(req: func.HttpRequest) -> func.HttpResponse:
    # TODO(adam): improve how to parameterize which server to connect to
    server_ip_query_parameter = "ip"
    server_ip = req.params.get(server_ip_query_parameter)
    if not server_ip:
        logging.info(
            "Query parameter not provided: %s", server_ip_query_parameter)
        return BadRequest(f"Please provider {server_ip_query_parameter} query parameter.")

    # TODO(adam): handle connection errors
    logging.debug("Connecting to RCON.")
    rcon_client = rcon.RCONClient(
        server_ip, 27015, get_factorio_rcon_password())

    logging.info("Connected to RCON.")

    # TODO(adam): handle command errors
    command = "/players online"
    logging.debug("Sending command: %s", command)
    response = rcon_client.send_command(command)

    logging.debug("Got RCON command response, parsing for player names.")
    users = re.findall(PATTERN, response)
    logging.debug("Found %d players", len(users))

    return Ok(json.dumps(users))

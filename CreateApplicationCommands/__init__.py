import logging
import os

import azure.functions as func
import requests
from DiscordWebhook.responses import Ok

APPLICATION_ID = "889284925247856690"
CLIENT_ID = "889284925247856690"

def get_client_secret() -> str:
    return os.environ["DISCORD_CLIENT_SECRET"]

def get_authentication_header() -> str:
    client_secret = get_client_secret()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "applications.commands.update"
    }

    response = requests.post("https://discord.com/api/oauth2/token", headers=headers, data=data, auth=(CLIENT_ID, client_secret))
    response.raise_for_status()
    response_json = response.json()
    token_type = response_json.get("token_type")
    access_token = response_json.get("access_token")
    return f"{token_type} {access_token}"


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    guild_id = req.params.get("guild_id")
    update_guild_commands = guild_id is not None
    if update_guild_commands:
        # update commands for a single guild
        logging.info(f"Updating guild commands for guild {guild_id}")
        relative_uri = f"/applications/{APPLICATION_ID}/guilds/{guild_id}/commands"
    else:
        # update global commands
        logging.info(f"Updating global commands")
        relative_uri = f"/applications/{APPLICATION_ID}/commands"

    commands = [
        {
            "name": "factorio",
            "type": 1,
            "description": "Manage a factorio server.",
            "options": [
                {
                    "name": "status",
                    "description": "Get the status of the server.",
                    "type": 1
                },
                {
                    "name": "start",
                    "description": "Start the server.",
                    "type": 1
                },
                {
                    "name": "stop",
                    "description": "Stop the server.",
                    "type": 1
                }
            ]
        }
    ]

    relative_uri = relative_uri.strip("/")
    url = f"https://discord.com/api/v8/{relative_uri}"

    headers = {
        "Authorization": get_authentication_header()
    }

    response = requests.put(url, headers=headers, json=commands)
    response.raise_for_status()
    return Ok(f"Created commands")

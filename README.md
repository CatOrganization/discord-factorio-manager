# Discord Factorio Manager
A discord bot which provides information about a headless factorio server.

## Setup
### Python
1. Install Python 3.9
1. Create a virtual environment. From the root of the repository, run:
    ```bash
    python -m venv .venv
    ```

1. Active the virtual environment.
    - Windows (PowerShell)
        ```powershell
        & .\.venv\Scripts\Activate.ps1
        ```

    - POSIX (Bash, zsh, or similar)
        ```bash
        source ./venv/bin/activate
        ```

1. Install pip packages:
    ```powershell
    python -m pip install -r requirements.txt
    ```

### Azure tools
1. Install the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
1. Install the [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local#install-the-azure-functions-core-tools)
1. Log in with Azure CLI
    ```powershell
    az login
    ```

1. Fetch Azure Functions settings
    ```powershell
    func azure functionapp fetch-app-settings factorio-bot
    ```

1. Modify local.settings.json
    - The value of `DISCORD_CLIENT_SECRET` should be set to the `CLIENT SECRET` from the [Discord application's OAuth2 settings](https://discord.com/developers/applications/889284925247856690/oauth2).
        - NOTE: Azure Key Vault references do not work when developing locally. If this restriction ever changes, this step would no longer be necessary.

## Developing
Using Visual Studio Code, start debugging using the "Attach to Python Functions" configuration (F5 by default).
The configuration will automatically launch the local Azure Functions runtime and attach a debugger.
The terminal output will show you available functions.

### Tools
#### Visual Studio Code
Visual Studio Code offers several extensions that aid with developing Azure Functions.
These are listed in [.vscode/extensions.json](.vscode/extensions.json).

#### ngrok
Debugging Discord webhooks using [ngrok](https://ngrok.com/) speeds up development significantly.
After launching the Functions host and attaching a debugger, use ngrok to start an HTTP tunnel to the default Azure Function port:

```powershell
ngrok http 7071
```

Copy the HTTPS endpoint provided by ngrok's output. Go to the [Discord application's settings](https://discord.com/developers/applications/889284925247856690/information) and update the Interactions Endpoint URL to ngrok HTTPS endpoint.

After saving the changes, Discord webhooks are forwarded to your local machine for debugging.

Navigating to http://localhost:4040 in a browser allows for closer inspection of webhook requests and responses, as well as replaying requests.

## Architecture
### Factorio Server
The factorio server manages a [headless factorio process](https://wiki.factorio.com/Multiplayer#Dedicated.2FHeadless_server).
A companion process monitors the factorio process to track its state and upload to blob storage.

#### State
The factorio companion process tracks the following information:
- Whether the VM is online, and how long it has been up.
- Whether the factorio process is running, and how long it has been up.
- Which players are online.

### Bot
The bot surfaces the state of the factorio process to a discord channel.

#### Slash commands
- `/factorio status`: Get the status of the server.
- `/factorio start`: Start the server.
- `/factorio stop`: Stop the server.

Slash commands are added to the discord application by sending a POST request to the `CreateApplicationCommands` Azure Function.

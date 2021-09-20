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

## Developing
Using Visual Studio Code, start debugging using the "Attach to Python Functions" configuration (F5 by default).
The configuration will automatically launch the local Azure Functions runtime and attach a debugger.
The terminal output will show you available functions.

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

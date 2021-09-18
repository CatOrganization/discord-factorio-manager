# Discord Factorio Manager
A discord bot which provides information about a headless factorio server.

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

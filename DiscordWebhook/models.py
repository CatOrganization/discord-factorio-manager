class CommandOptionType:
    """
    An option type for an application command.
    
    https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-type
    """
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 9
    MENTIONABLE = 9
    NUMBER = 10

# game-matchmaker

Project - game-matchmaker 

Bot commands - 
On-message(user input): Commands are used by messaging using the format !<command-name> in a channel where the bot is running
    
    core commands -
        1) !LFG <game-name> <max no.of players> (additional options may be included later such as rank filters, role)
            Creates a unique game id which other players can join (see Join command) till the max number of players is reached
        2) !Join <match-id> <player-name>
            Adds the given player name to the given match (if not full) 
        5) !Leave <match-id> <player-name>
            Removes the given player name from the given match
    info functions
        1) List all available command options (to be implemented)
        2) Detailed help for each command (to be implemented)


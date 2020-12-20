# game-matchmaker

Project - game-matchmaker 

Bot Behaviours - 

    core functions -
        1) On-message(user input):  !LFG <game-name> <no.of player> (additional options can be included such as rank,role)
        2) post LFG request with unique id on channel, maintains player queue 
        3) On-message(user-input) - !Join <LFG-request-id> 
        5) On-message(user-input) - !Leave <LFG-request-id>
        6) Updates player queue on Join/Leave

    info functions
        1) List all available command options
        2) detailed help for each command


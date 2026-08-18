class Command:
    def __init__(self, desc, brief, param):
        self.description = desc
        self.brief = brief
        self.parameters = param

start = Command("Creates a new session with a given name and number of tables.", "Makes a new session",
                {"event_name": "The name of the session (event code, event name, etc.).",
                 "number_of_tables": "The number of tables available in the main seating area."})

add = Command("Adds a player with a given name to a specified bracket.", "Adds a player to a bracket",
                  {"bracket": "The bracket you want the player added to.",
                   "name": "The name of the player being added."})

blkAdd = Command("Adds multiple players to the same bracket.", "Adds multiple players to a bracket",
                      {"bracket": "The bracket you want to add players to.",
                       "player 1": "The name of the first player added.",
                       "players 2...n": "Additional players added to the bracket"})

rm = Command("Removes a player from the session regardless of bracket.", "Removes a player",
                     {"name": "The name of the player being removed."})

change = Command("Changes the bracket of a given player.", "Changes a player's bracket",
                            {"bracket": "The bracket the player is being moved to.",
                             "name": "The name of the player being moved."})

group = Command("Creates a group of players in the same bracket (will create new players if they aren't already there).", "Creates a group in a bracket",
                    {"bracket": "The bracket the group is being made in.",
                     "players 1 & 2": "Player names. Each group must include at least 2 players.",
                     "players 3 & 4": "Additional player names."})

pCount = Command("Gives a count of players in a given bracket (or all brackets if none is specified).", "Gives a count of players on one or all brackets",
                           {"bracket": "The bracket a count is required for. Leave blank for all brackets."})

pList = Command("Lists all current players in a given bracket (or all brackets if none is specified).", "List players in one or all brackets",
                           {"bracket": "The bracket a player list is required for. Leave blank for all brackets."})

brkList = Command("Lists the names and indexes of all brackets.", "Lists all current brackets", None)

startRound = Command("Starts a new round of pods and lists the table arrangements.", "Starts a new round of pods", None)

end = Command(
    "Ends the current session, removing all current players and brackets.",
    "Ends the current session",
    None,
)

commandList = {
    "start": start,
    "add": add,
    "addBulk": blkAdd,
    "remove": rm,
    "changeBracket": change,
    "group": group,
    "playerCount": pCount,
    "playerList": pList,
    "listBrackets": brkList,
    "startRound": startRound,
    "end": end
}

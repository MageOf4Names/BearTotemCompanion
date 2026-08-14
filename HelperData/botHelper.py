commandList = {
    "start": """Creates a new session with a given number of tables and name.
__Usage:__ `!start {tables} {name}`
- tables *(optional)*: The number of tables available in the main seating area.
- name *(optional)*: The name of the session (event code, event name, etc.).""",

    "add": """Adds a player with a given name to a specified bracket.
__Usage:__ `!add [bracket] [name]`
- bracket: The bracket you want the player added to.
- The name of the player being added.""",

    "addBulk": """Adds multiple players to the same bracket.
__Usage:__ `!addBulk [bracket] [player 1] {player 2} ...`
- bracket: The bracket you want to add players to.
- player 1: The name of the first player added.
- players 2...n *(optional)*: Additional players added to the bracket""",

    "remove": """Removes a player from the session regardless of bracket.
__Usage:__ `!add [name]`
- name: The name of the player being removed.""",

    "changeBracket": """Changes the bracket of a given player.
__Usage:__ `!changeBracket [new bracket] [player]`
- new bracket: The bracket the player is being moved to.
- player: The name of the player being moved.""",

    "group": """Creates a group of players in the same bracket (will create new players if they aren't already there).
__Usage:__ `!group [bracket] [player 1] [player 2] {player 3} {player 4}`
- bracket: The bracket the group is being made in.
- players 1 & 2: Player names. Each group must include at least 2 players.
- players 3 & 4 *(optional)*: Additional player names.""",

    "playerCount": """Gives a count of players in a given bracket (or all brackets if none is specified).
__Usage:__ `!playerCount {bracket}`
- bracket *(optional)*: The bracket a count is required for. Leave blank for all brackets.""",

    "listPlayers": """Lists all current players in a given bracket (or all brackets if none is specified).
__Usage:__ `!listPlayers {bracket}`
- bracket *(optional)*: The bracket a player list is required for. Leave blank for all brackets.""",

    "listBrackets": """Lists the names and indexes of all brackets.
__Usage:__ `!listBrackets`""",

    "startRound": """Starts a new round of pods and lists the table arrangements.
__Usage:__ `!startRound`""",

    "end": """Ends the current session, removing all current players and brackets.
__Usage:__ `!end""",
}

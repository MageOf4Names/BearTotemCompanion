# Bear Totem Companion Bot

## Basic concept:

- A bot that creates a session (with or without a game code) and sorts out pods with the given amount of people.
- Once a session is created, add people one by one or via bulk insert.
- Occassionaly add groups that need to be sorted into a pod together.
- Once everyone has been added, start round 1

  - Create as many 4 pods as possible (while not leaving a remainder of 2 players) using as many tables upstairs as possible
  - Sort remaining players into 3 pods and/or downstairs tables if necessary
- After round 1, re-randomize with the following rules:

  - No one can be in a 3 pod for both rounds
  - No one can be downstairs both rounds
  - Groups remain together

## Command outlines:

#### Create session

- !StartSession {tables} {code}

  - creates a blank session using 2 optional parameters
  - tables: The number of tables available upstairs
  - code: The event code for that given night (implemented only if the bot sends out an announcement with the game code)

#### Add players to a session

- !Add [bracket] [player]

  - Adds a player with a given name to the current session
  - bracket: The bracket that player is participating in
  - player: The name of the player (MUST BE UNIQUE!)

#### Bulk addition of players

- !BulkAdd [bracket] [player1] {player2} ...
  - Adds a variable number of players to the current session
  - bracket: The bracket the players are participating in
  - player1...n: The names of players being inserted

#### Grouping players

- !MakeGroup [player1] [player2] {player3} {player4}
  - Creates a group of up to 4 players that will be sorted together
  - player1 & player2: Mandatory inputs (a group of 1 can be ignored)
  - player3 & player4: Optional parameters for additional group members

#### Start a round

- !RoundStart
  - Randomly assigns people to tables
  - First time called, only worry about keeping groups together
  - Subsequent calls, follow rules for avoiding players having multiple games in a 3 pod/downstairs

#### Finishing a session

- !FinishSession
  - Finishes the current session and resets the relevant values
  - Will need to take a name or ID parameter if extended to support multiple sessions.

## Implementation:

#### Create session:

Creates a global session object for the server. The session will track brackets, players, groups, and how many rounds have elapsed

###### Session object:

**Attributes:**

- Name (String): The name of the session. Could be an identifier, or an event code.
- Brackets (Bracket[]): An array of bracket objects. One for each bracket being played that night (always creates 3 by default)
- Tables (Int): The number of tables available in the main seating area
- Round (Int): The current number of initiated rounds.

**Methods:**

- SetTables(int tableCount): Sets the session's number of available to tableCount
- AddPlayer(string name, int bracket): Adds a new player with a given name to the given bracket
- ChangeBracket(string player, int bracket): Changes a player with name to the given bracket
- CreateBracket(string name): Creates a new bracket named "name" and adds it to the end of the array
- PlayerCount(int bracket): Gives the player count for a specific bracket. If no bracket is given, list all counts instead
- StartRound(): Goes through each bracket and assigns the players tables starting with the available main seating area then following secondary seating
- ListPlayers(int bracket): Lists all the available players in a given bracket. Displays all brackets if none is specified.

###### Bracket Object:

**Attributes:**

- Name (String): Display name for the bracket. Used for displaying table groupings
- Players (Player[]): A list of player objects. One for each participating in that particular bracket
- Groups (Player[][]): A list of player lists specifying who should be sat together
- Pods (Pod[]): A list of pod objects that gets cleared at the start of each round and holds the groupings for tables
- Up (Boolean): A boolean value to determine if a bracket should be seated upstairs or downstairs first

**Methods:**

- AddPlayer(string name): Adds a new player to the bracket with a given name
- RemovePlayer(string name): Removes a given player from the bracket
- CreateGroup(string... names): Creates a grouping of 1-4 players and adds it to the groups list for that bracket
- StartRound(int tables): Randomizes the list of players, determines the number and count of pods, and sudo-randomly assigns players to tables while avoiding certain rules
  - First, empty the pods array and mark every player as unseated
  - Based on the number of players, populate the pods array with the appropriate number of correctly-sized pods. Based on the # Players % 4:
    - 0: No 3 pods needed, create players/4 full pods
    - 1: Create (players/4 - 2) full pods followed by 3 3-pods
    - 2: Create (players/4 - 1) full pods followed by 2 3-pods
    - 3: Create players/4 full pods followed by 1 3-pod
  - Sort Players by the number of games they've had in a 3-pod and downstairs and ensure those players are assigned tables randomly first in upstairs 4 pods
    - If a player has played more 3 pods than average, sort them among the 4 pods
    - If a player has played more games downstairs than average, sort them upstairs
  - Fill in the rest of the tables randomly using the remaining players
    - If a player is seated downstairs, increment their value
    - If a player is seated in a 3-pod, increment their value

###### Player Object:

**Attributes:**

- Name (string): Name of the player
- Threes (int): Number of games played in a 3 pod that night
- DownCount (int): Number of games played downstairs that night

**Methods:**

- Seat(bool three, bool down): Sets the player's seated flag to true and increments the threes and/or downCount attributes appropriately based on pod type

###### Pod Object:

**Attributes:**

- Name (string): The name of the pod (typically a table name)
- MaxSize (int): The maximum size of the pod (3 or 4)
- Players (Player[]): The names of the players in the pod

**Methods:**

- AddPlayer(Player p): Adds the given player to the pod

#### Adding players:

#### Bulk addition:

#### Implementing groups:

#### Starting a round:

##### Round 1:

##### Round 2 and on:

#### Finishing a session:

## Potential additions:

- Creating more than one session simultaneously
  - Would need to add a name field to the session command.
- Saving regular members for bulk addition.
  - Potentially saving them numerically and having a command to add them using those keys.
- Automatically sending out an announcement with the game code if a session was created with one.

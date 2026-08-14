# Welcome to the Bear Totem Companion app

## Quick links

1. [Project Background](https://github.com/MageOf4Names/BearTotemCompanion#project-background)
2. [Current Release](https://github.com/MageOf4Names/BearTotemCompanion#current-release-01)
3. [Command List](https://github.com/MageOf4Names/BearTotemCompanion#command-list)
4. [Cloning and Running the Project](https://github.com/MageOf4Names/BearTotemCompanion#cloning-and-running-the-project)

## Project Background

This is a discord bot intended to be the companion app for my LGS to help them sort MTG Commander pods automatically. While the application is general enough to be repurposed for (theoretically) any game store, there are some special rules that make this unique including:

- Multiple seating areas:

  - Bear Totem includes two main seating areas. One upstairs with the game store, and another downstairs in the cafe. As such, the goal of the bot is to randomize pods in such a way that players do not have continuous games in the downstairs area.
- Variable players:

  - As Bear Totem's commander nights are open to the community, there is no guarantee that the number of players is evenly divisible by 4. As a result, some players may be sorted into smaller pods. The bot seeks to ensure that no player is continuously sat in smaller pods.
- Multiple play brackets:

  - Bear Totem offers multiple levels of play including categories like "Play to win" and "Play for fun". As such, the bot needs to accomodate multiple play brackets that all sort players automatically.
- Grouping:

  - Some players attend commander nights in groups and like to be sat together. As a result, the bot needs to be able to maintain these groupings.

## Current Release (0.1)

The bot is currently in it's first workable state. While functional, there are some edges to smooth over. As it stands, the currently has the following functionality:

- Start a session with a set number of tables and an event name
- Adding (one-by-one or in bulk) players to a specific bracket
- Removing a player from the session or changing their bracket
- Forming groups of players within a bracket
- Getting a player count/list from one or all brackets
- List all available brackets
- Start a round by creating and randomly seeding pods while following the rules listed above
- End a round and clear all player, group, and bracket data

## Future plans

### Intended features

These are features that I am actively working on adding to the bot's functionality. Many of these will probably be needed before a 1.0 release.

- Tracking a global list of players to avoid any player from being listed in multiple brackets
- Improving the help function to be more user-friendly
- Implementing command completion to reduce the amount of accidental errors while trying to use commands
- Restricting use of the bot to a whitelist of users/roles on a per-server level
- Adding the ability to send placement messages to a different channel so the seating can be shared without having to see the command inputs
- Adding presets to commands like !start to reduce the amounts of input needed

### Potential Features

These are features that don't necessarily fit the specific use-case for this project, but may be a nice expansion of features that the shop could use:

- Adding, removing, or editing brackets
- Seeing and editing each bracket's seating preset (whether they are defaulted to upstairs/downstairs)
- Setting table counts after a session has started
- Adding flex-tables (tables that could hold one group of 4 or 2 groups of three)

## Command List

### start

__Description:__ Creates a new session with a given number of tables and name.

__Usage:__ `!start {tables} {name}`

- tables *(optional)*: The number of tables available in the main seating area.
- name *(optional)*: The name of the session (event code, event name, etc.).

### add

__Description:__ Adds a player with a given name to a specified bracket.

__Usage:__ `!add [bracket] [name]`

- bracket: The bracket you want the player added to.
- The name of the player being added.

### addBulk

__Description:__ Adds multiple players to the same bracket.

__Usage:__ `!addBulk [bracket] [player 1] {player 2} ...`

- bracket: The bracket you want to add players to.
- player 1: The name of the first player added.
- players 2...n *(optional)*: Additional players added to the bracket

### remove

__Description:__ Removes a player from the session regardless of bracket.

__Usage:__ `!add [name]`

- name: The name of the player being removed.

### changeBracket

__Description:__ Changes the bracket of a given player.

__Usage:__ `!changeBracket [new bracket] [player]`

- new bracket: The bracket the player is being moved to.
- player: The name of the player being moved.

### group

__Description:__ Creates a group of players in the same bracket (will create new players if they aren't already there).

__Usage:__ `!group [bracket] [player 1] [player 2] {player 3} {player 4}`

- bracket: The bracket the group is being made in.
- players 1 & 2: Player names. Each group must include at least 2 players.
- players 3 & 4 *(optional)*: Additional player names.

### playerCount

__Description:__ Gives a count of players in a given bracket (or all brackets if none is specified).

__Usage:__ `!playerCount {bracket}`

- bracket *(optional)*: The bracket a count is required for. Leave blank for all brackets.

### listPlayers

__Description:__ Lists all current players in a given bracket (or all brackets if none is specified).

__Usage:__ `!listPlayers {bracket}`

- bracket *(optional)*: The bracket a player list is required for. Leave blank for all brackets.

### listBrackets

__Description:__ Lists the names and indexes of all brackets.

__Usage:__ `!listBrackets`

### startRound

__Description:__ Starts a new round of pods and lists the table arrangements.

__Usage:__ `!startRound`

### end

__Description:__ Ends the current session, removing all current players and brackets.

__Usage:__ `!end`

## Cloning and Running the Project

### Out of the box

This GitHub repository lacks the bot keys and other environment variable to be able to run out of the box. While it is technically possible to repurpose for your own bot, those variables will need to be reproduced by hand

### Ideas for repurposing

While the bot itself isn't runnable just from cloning, many of the objects and interfaces used by the bot code are. The Player, Pod, Bracket, and Session objects are all fully fucntional (as you'll see, the bot code is little more than a wrapper for those objects and some error checking). My suggestion would be to spend some time understanding the various functions in each object (or just session if you're in a hurry to get up and going), and write your own wrapper/application around the Session object. While Session is the only object you really need to interact with to get this project up and going, I would highly suggest diving into Bracket, Pod, and Player to fully understand the workings of each object.

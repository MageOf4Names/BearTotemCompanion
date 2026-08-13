# General use exception for a player not being found where it was expected to be.
class PlayerNotFound(Exception):
    pass

class SeatingError(Exception):
    pass

class PodOverflowError(Exception):
    pass

class UnderfullBracketError(Exception):
    pass

class OverfullGroupError(Exception):
    pass

class UnderfullGroupError(Exception):
    pass

class PlayerAlreadyGroupedError(Exception):
    pass

class PlayerExistsError(Exception):
    pass
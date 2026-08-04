# General use exception for a player not being found where it was expected to be.
class PlayerNotFound(Exception):
    pass

class SeatingError(Exception):
    pass

class PodOverflowError(Exception):
    pass

class OverfullGroupError(Exception):
    pass
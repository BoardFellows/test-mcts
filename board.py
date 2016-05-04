class Board(object):
    """Board Object Encapsulates Game Rules."""
    # state must be hashable, and equivalent states hash to same value.

    def start(self):
        """Return Representation of starting state of game."""
        pass

    def current_player(self, state):
        """Take current state of game and return player's number."""
        pass

    def next_state(self, state, play):
        """Take the current state, and the next play, and update state."""
        pass

    def legal_plays(self, state_history):
        """Take sequence of game states representing full move history.

        Return list of legal moves for current player.
        """
        pass

    def history(self, state_history):
        """If game is won, return player number.

        If game is ongoing, return 0. If game is tied, return -1.
        Take sequence of full move history.
        """
        pass

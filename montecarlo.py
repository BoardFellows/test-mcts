import datetime
from random import choice


class MonteCarlo(object):
    """AI and handling AI Tree Search."""

    def __init__(self, board, **kwargs):
        """Initialize game states and stats tables.

        Takes a board and optional kwargs.
        """
        # Board gives AI info on where game is going/what moves it
        # can make
        self.board = board
        # list of states
        # Authoritive record of game history
        self.states = []
        # counts for every day state being tracked
        # keys are all tuples of (player, state)
        self.wins = {}
        self.plays = {}

        self.C = kwargs.get('C', 1.4)


    def update(self, state):
        """Take a game state and append it to the history."""
        self.states.append(state)

    def get_play(self):
        """Calculate best available move and return it."""
        self.max_depth = 0
        state = self.states[-1]
        player = self.board.current_player(state)
        legal = self.board.legal_plays(self.states[:])

        # if no legal moves, return
        if not legal:
            return
        # if only one legal move, do that
        if len(legal) == 1:
            return legal[0]

        # num of game simulations run
        games = 0
        begin_time = datetime.datetime.utc.now()
        # Runs until given time runs out
        while datetime.datetime.utc.now() - begin_time < self.calc_time:
            self.run_simulation()
            games += 1

        move_states = [(p, self.board.next_state(state, p)) for p in legal]

        # print number of games, and time elapsed.
        print(games, datetime.datetime.utc.now() - begin_time)

        # get highest percentage move
        percent_wins, move = max(
            (self.wins.get((player, S), 0) /
                self.plays.get((player, S), 1), P)
            for P, S in move_states
        )

        for x in sorted(
            ((100 * self.wins.get((player, S), 0) /
              self.plays.get((player, S), 1),
              self.wins.get((player, S), 0),
              self.plays.get((player, S), 0), p)
             for p, S in move_states),
            reverse=True
        ):
            print("{3}: {0:.2f}% ({1} / {2})".format(*x))

        print("Maximum depth searched:", self.max_depth)

        return move

    def run_simulation(self):
        """Play out random game from current position.

        Updates the stats tables.
        """
        # make local variables instead of attribute lookup
        plays, wins = self.plays, self.wins
        visited_states = set()
        states_copy = self.states[:]
        state = states_copy[-1]
        player = self.board.current_player(state)

        expand = True

        # TODO: MAKE NOT RANDOM
        # selects move using either UCB1 or random chance
        # for move in max moves
        for move in range(1, self.max_moves + 1):
            # find legal loves at that state in game
            legal = self.board.legal_plays(states_copy)
            # make a choice
            moves_states = [(p, self.board.next_state(state, p)) for p in legal]
            # play = choice(legal)
            # find next state
            # state = self.board.next_state(state, play)

            if all(plays.get((player, S)) for p, S in moves_states):
                # If we have stats on all of the legal moves here, use them.
                log_total = log(
                    sum(plays[(player, S)] for p, S in moves_states))
                value, move, state = max(
                    ((wins[(player, S)] / plays[(player, S)]) +
                     self.C * sqrt(log_total / plays[(player, S)]), p, S)
                    for p, S in moves_states
                )
            else:
                # Otherwise, just make an arbitrary decision.
                move, state = choice(moves_states)
            # add state to list of states
            states_copy.append(state)

            # player who moved into state
            # if you want to expand children and
            # if this move has not been made by this player
            if expand and (player, state) not in self.plays:
                # if current state is first unknown state
                # turn off expand
                expand = False
                # add player and state to wins/plays and set at zero
                # start keeping track of this player/state
                self.plays[(player, state)] = 0
                self.wins[(player, state)] = 0
                if t > self.max_depth:
                    self.max_depth = t
            # update visited states with current player/state
            visited_states.add((player, state))

            # get current player
            player = self.board.current_player(state)
            # get winner if there is one
            winner = self.board.winner(states_copy)
            if winner:
                # if winner, the simulation is over
                break
        # pick first unknown game state and add it to table

        # after simulation is over, look over visited states
        # update totals at the end
        # backpropagation
        for player, state in visited_states:
            if (player, state) not in self.plays:
                # if state was never played, ignore
                continue
            # increase that states num of plays
            self.plays[(player, state)] += 1
            if player == winner:
                # if that state resulted in a win condition
                # update wins
                self.wins[(player, state)] += 1

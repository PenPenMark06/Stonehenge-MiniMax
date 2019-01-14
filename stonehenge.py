"""
Gameclass of the stonehenge game
"""
import math
from game import Game
from stone_state import StonehengeState


class StonehengeGame(Game):
    """
    A game of stonehenge when the game is initialized
    """

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.
        """

        str_game_size = input("Input the size of the game board: ")
        # game_size = 1
        game_size = int(str_game_size)
        self.game_size = game_size
        alph = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                'W', 'X', 'Y', 'Z']

        i = 0
        n = 2

        self.h_rows = []
        self.new_lists = []

        while i < game_size + 1:

            self.rows = []
            if i == game_size:
                for c in range(game_size):
                    self.rows.append(alph.pop(0))
            else:
                for c in range(n):
                    self.rows.append(alph.pop(0))

            self.h_rows.append(self.rows)
            n += 1
            i += 1

        # Create green line connections, the vertical left slanted lines
        # Create the empty lists same number as the length of the list of hlists
        self.vl_rows = []
        for i in range(len(self.h_rows)):
            self.vl_rows.append([])
        # Append the items to the list created by following the h_rows elements
        c = 0
        while c < len(self.h_rows):
            i = 0 if c < len(self.h_rows) - 1 else 1
            for elements in self.h_rows[c]:
                self.vl_rows[i].append(elements)
                i += 1
            c += 1

        # Do the same thing but from the opposite side to make a vr lines
        self.vr_rows = []
        for i in range(len(self.h_rows)):
            self.vr_rows.append([])

        x = len(self.h_rows) - 1

        while x >= 0:
            if x == len(self.h_rows) - 1:
                i = 0
            else:
                i = (game_size + 1) - len(self.h_rows[x]) \
                    if len(self.h_rows[x]) < len(self.h_rows[x + 1]) else 0
            for elements in self.h_rows[x]:
                self.vr_rows[i].append(elements)
                i += 1
            x -= 1

        i = 0
        while i < len(self.h_rows):
            if i == 0:
                self.new_lists.append(['@', '@'])

            if len(self.h_rows[i]) == game_size + 1:
                self.new_lists.append(['@'] + self.h_rows[i])
                self.new_lists.append(
                    [] + ['\\', '/'] * (len(self.h_rows[i]) - 1) + ['\\'])
            elif i == len(self.h_rows) - 1:
                self.new_lists.append(['@'] + self.h_rows[i] + ['@'])
                self.new_lists.append([] + ['@'] * game_size)
            else:
                self.new_lists.append(['@'] + self.h_rows[i] + ['@'])
                if i != 0 and len(self.h_rows[i]) < len(self.h_rows[i - 1]):
                    self.new_lists.append(
                        [] + ['\\', '/'] * len(self.h_rows[i]) + ['/'])
                else:
                    self.new_lists.append(
                        [] + ['/', '\\'] * len(self.h_rows[i]) + ['/'])

            i += 1

        info = [self.h_rows, self.vl_rows, self.vr_rows, self.new_lists]

        self.current_state = \
            StonehengeState(p1_starts, game_size, info, {'p1': 0, 'p2': 0})

    def get_instructions(self) -> str:
        """
        Return the instructions for this Game.
        """
        return "Welcome to Stonehenge Game!!"

    def is_over(self, state: StonehengeState) -> bool:
        """
        Return whether or not this game is over at state.
        """

        if self.current_state.get_current_player_name() == 'p1':
            previous_player = 'p2'
        else:
            previous_player = 'p1'

        total_line = (self.game_size + 1) * 3
        win_line = math.ceil(total_line / 2)
        return len(self.current_state.get_possible_moves()) == 0 or \
               self.current_state.lines_got[previous_player] >= win_line

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.
        """

        total_line = (self.game_size + 1) * 3

        return self.current_state.lines_got[player] >= math.ceil(total_line/2)

    def str_to_move(self, string: str) -> str:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.
        """
        alph = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z']
        if string not in alph:
            return 'Wrong move boy'

        return string.upper()

if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")

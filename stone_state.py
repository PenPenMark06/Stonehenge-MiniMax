"""
subclass of the current_state, particulary for stonehenge game
"""

import math
import copy
from game_state import GameState


class StonehengeState(GameState):
    """
    Current state of the single stonehenge game
    """

    from typing import Any

    def __init__(self, is_p1_turn: bool, game_size: int, info: list,
                 lines_got: dict) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.

        """
        self.p1_turn = is_p1_turn
        self.game_size = game_size
        self.h_rows = info[0]
        self.v1_rows = info[1]
        self.vr_rows = info[2]
        self.new_lists = info[3]
        self.lines_got = lines_got

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.

        """
        original_state = self.make_original(self.game_size)

        board_state = ''

        spacing = 8 + (2 * (self.game_size - 2))
        n = 0
        i = 0
        board_state += ' ' * spacing + str(self.new_lists[i][n]) + \
                       ' ' * 3 + str(self.new_lists[i][n + 1]) + '\n'
        board_state += ' ' * (spacing - 1) + '/' + ' ' * 3 + '/' + '\n'
        i += 1

        while i < len(self.new_lists) - 1:
            if i % 2 == 1:
                board_state = self.helper_recursive_nest(
                    original_state, board_state, i)

            else:
                board_state += ' ' * (((self.game_size + 1 -
                                        (len(self.new_lists[i - 1]) - 2))
                                       * 2) + 3)
                for n in range(len(self.new_lists[i])):
                    board_state += str(self.new_lists[i][n]) + ' '
                board_state += '\n'
            i += 1

        board_state += ' ' * (((self.game_size + 1 -
                                (len(self.new_lists[i - 1]) - 2)) * 2) + 5)
        for n in range(self.game_size):
            board_state += '\\' + ' ' * 3

        board_state += '\n'
        board_state += ' ' * (((self.game_size + 1 -
                                (len(self.new_lists[i - 1]) - 2)) * 2) + 6)
        for n in range(self.game_size):
            board_state += str(self.new_lists[i][n]) + ' ' * 3

        return board_state

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.
        """
        alph = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y', 'Z']

        possible_moves = []
        for items in self.h_rows:
            for elements in items:
                if elements in alph:
                    possible_moves.append(elements)

        total_line = (self.game_size + 1) * 3
        win_line = math.ceil(total_line/2)

        if self.lines_got['p1'] >= win_line or self.lines_got['p2'] >= win_line:
            return []

        return possible_moves

    def get_current_player_name(self) -> str:
        """
        Return 'p1' if the current player is Player 1, and 'p2' if the current
        player is Player 2.
        """
        if self.p1_turn:
            return 'p1'
        return 'p2'

    def make_move(self, move: str) -> 'StonehengeState':
        """
        Return the GameState that results from applying move to this GameState.

        """
        original_state = self.make_original(self.game_size)
        info = [self.h_rows, self.v1_rows, self.vr_rows, self.new_lists]
        new_info = copy.deepcopy(info)
        i = 0

        # Changing the value of each list depending on the move

        while i < len(new_info):
            s = 0
            while s < len(new_info[i]):
                self.assign_name_helper(i, s, new_info, move)

                s += 1
            i += 1

        # check for the horizontal change of the lines marks
        ceil = math.ceil
        n = 0
        # check horizontal first

        while n < len(new_info[3]):
            if original_state[3][n][-1] != '@' and \
                    n == self.game_size * 2 - 1:
                if new_info[3][n][1:].count(1) >= \
                        ceil((len(new_info[3][n][1:])) / 2) and \
                        not isinstance(new_info[3][n][0], int):
                    new_info[3][n][0] = 1
                    self.lines_got['p1'] += 1
                elif new_info[3][n][1:].count(2) >= \
                        ceil((len(new_info[3][n][1:])) / 2) and \
                        not isinstance(new_info[3][n][0], int):
                    new_info[3][n][0] = 2
                    self.lines_got['p2'] += 1
            elif any(x != '@' for x in original_state[3][n]):
                if new_info[3][n][1:-1].count(1) >= \
                        ceil(len(new_info[3][n][1:-1]) / 2) and \
                        not isinstance(new_info[3][n][0], int):
                    new_info[3][n][0] = 1
                    self.lines_got['p1'] += 1
                elif new_info[3][n][1:-1].count(2) >= \
                        ceil((len(new_info[3][n][1:-1])) / 2) and \
                        not isinstance(new_info[3][n][0], int):
                    new_info[3][n][0] = 2
                    self.lines_got['p2'] += 1

            n += 1

        # Check for the vl, green line
            # now check vl line taken or not

        n = 0
        move_first = ''
        for items in original_state[1]:
            if move in items:
                move_first = items[0]

        while n < len(new_info[1]):
            if new_info[1][n].count(1) >= \
                    ceil(len(new_info[1][n]) / 2) and \
                    self.get_current_player_name() == 'p1':
                self.helper_assignment(n, move_first, move, new_info)

            if new_info[1][n].count(2) >= ceil((len(new_info[1][n])) / 2) and \
                    self.get_current_player_name() == 'p2':
                self.helper_assignment2(n, move_first, move, new_info)

            n += 1

        # lastly check for vr, the blue line
        n = 0
        while n < len(new_info[2]):
            if new_info[2][n].count(1) >= \
                    ceil((len(new_info[2][n])) / 2) and \
                    self.get_current_player_name() == 'p1':
                self.helper_assignment3(n, new_info)

            if new_info[2][n].count(2) >= \
                    ceil((len(new_info[2][n])) / 2) and \
                    self.get_current_player_name() == 'p2':
                self.helper_assignment4(n, new_info)

            n += 1

        if self.p1_turn:
            p1_next = False
        else:
            p1_next = True

        new_state = \
            StonehengeState(p1_next, self.game_size, new_info, self.lines_got)
        return new_state

    def is_valid_move(self, move: Any) -> bool:
        """
        Return whether move is a valid move for this GameState.
        """
        return move in self.get_possible_moves()

    def __repr__(self) -> str:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        raise 'currently it is ' + self.get_current_player_name() + \
              ' turn and here is the board: \n' + self.__str__()

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        """
        fake_current = copy.deepcopy(self)
        moves = self.get_possible_moves()
        total_line = (self.game_size + 1) * 3
        win_line = math.ceil(total_line / 2)
        next_states = []
        eval_next_states = {}

        if self.get_current_player_name() == 'p1':
            previous_player = 'p2'
        else:
            previous_player = 'p1'

        for move in moves:
            new_state = fake_current.make_move(move)
            if new_state.lines_got[previous_player] >= win_line:
                return 1
            next_states.append(new_state)

        for states in next_states:
            eval_next_states[states] = []
            for move in states.get_possible_moves():
                newer_state = states.make_move(move)
                if newer_state.lines_got[states.get_current_player_name()] \
                        >= win_line:
                    eval_next_states[states].append(-1)
                else:
                    eval_next_states[states].append(1)

        for keys in eval_next_states:
            if all(x == 1 for x in eval_next_states[keys]):
                return 0

        return -1

    def make_original(self, game_size: int) -> list:
        """
        Helper function of make move, Generate the original state of the game
        For assesing which @ to change from the modifying list

        """
        alph = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y', 'Z']

        i = 0
        n = 2

        h_rows = []
        new_lists = []

        while i < game_size + 1:

            rows = []
            if i == game_size:
                for c in range(game_size):
                    rows.append(alph.pop(0))
            else:
                for c in range(n):
                    rows.append(alph.pop(0))

            h_rows.append(rows)
            n += 1
            i += 1

        # Create green line connections, the vertical left slanted lines
        # Create the empty lists same number as the length of the list of hlists

        vl_rows = []
        for i in range(len(self.h_rows)):
            vl_rows.append([])
        # Append the items to the list created by following the h_rows elements
        c = 0
        while c < len(h_rows):
            i = 0 if c < len(h_rows) - 1 else 1
            for elements in h_rows[c]:
                vl_rows[i].append(elements)
                i += 1
            c += 1

        # Do the same thing but from the opposite side to make a blue lines
        vr_rows = []
        for i in range(len(h_rows)):
            vr_rows.append([])

        x = len(h_rows) - 1

        while x >= 0:
            if x == len(h_rows) - 1:
                i = 0
            else:
                i = (game_size + 1) - len(h_rows[x]) if \
                    len(h_rows[x]) < len(h_rows[x + 1]) else 0
            for elements in h_rows[x]:
                vr_rows[i].append(elements)
                i += 1
            x -= 1

        i = 0
        while i < len(h_rows):
            if i == 0:
                new_lists.append(['@', '@'])

            if len(h_rows[i]) == game_size + 1:
                new_lists.append(['@'] + h_rows[i])
                new_lists.append([] + ['\\', '/'] *
                                 (len(h_rows[i]) - 1) + ['\\'])
            elif i == len(h_rows) - 1:
                new_lists.append(['@'] + h_rows[i] + ['@'])
                new_lists.append([] + ['@'] * game_size)
            else:
                new_lists.append(['@'] + h_rows[i] + ['@'])
                if i != 0 and len(h_rows[i]) < len(h_rows[i - 1]):
                    new_lists.append([] + ['\\', '/'] * len(h_rows[i]) + ['/'])
                else:
                    new_lists.append([] + ['/', '\\'] * len(h_rows[i]) + ['/'])

            i += 1

        info = [h_rows, vl_rows, vr_rows, new_lists]
        return info

    def helper_recursive_nest(self, original_state: list,
                              board_state: str, i: int) -> str:
        """
        Helper function for string representation,
        method __str__ as it was nested too much
        """

        alph = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y', 'Z']

        if len(self.h_rows[i // 2]) != self.game_size + 1:
            board_state += ' ' * ((self.game_size + 1 -
                                   (len(self.new_lists[i]) - 2)) * 2)

        for n in range(len(self.new_lists[i])):

            if n != len(self.new_lists[i]) - 1 or \
                    self.new_lists[i][n] in alph or \
                    original_state[3][i][-1] != '@':
                board_state += str(self.new_lists[i][n])
                if n < len(self.new_lists[i]) - 2:
                    board_state += ' - '
                elif len(self.h_rows[i // 2]) == self.game_size + 1 and \
                        n != len(self.new_lists[i]) - 1:
                    board_state += ' - '

            else:
                board_state += ' ' * 3 + str(self.new_lists[i][n])
        board_state += '\n'

        return board_state

    def assign_name_helper(self, i: int, s: int,
                           new_info: list, move: str) -> None:
        """
        Helper funtction for modifying the new_list
        """
        if move in new_info[i][s]:
            n = 0
            while n < len(new_info[i][s]):
                if new_info[i][s][n] == move:
                    new_info[i][s][n] = int(
                        self.get_current_player_name()[-1])
                n += 1

    def helper_assignment(self, n: int, move_first: str,
                          move: str, new_info: list) -> None:
        """
        Helper fucntion for assigning the number to horizontal list
        """
        original_state = self.make_original(self.game_size)
        c = 0
        if n < 2:
            if n == 0 and not isinstance(new_info[3][0][0], int):
                new_info[3][0][0] = 1
                self.lines_got['p1'] += 1
            elif n == 1 and not isinstance(new_info[3][0][1], int):
                new_info[3][0][1] = 1
                self.lines_got['p1'] += 1
        elif n >= 2 and move in original_state[1][n]:
            for i in range(len(original_state[3])):
                if move_first in original_state[3][i] and i != 1:
                    c = i - 2
                elif move_first in original_state[3][i] and i == 1:
                    c = i - 1
            if not isinstance(new_info[3][c][-1], int):
                new_info[3][c][-1] = 1
                self.lines_got['p1'] += 1

    def helper_assignment2(self, n: int, move_first: str,
                           move: str, new_info: list) -> None:
        """
        Helper function for assigning the number(player number) to
        vertical ley line for player 2
        """

        original_state = self.make_original(self.game_size)
        c = 0

        if n < 2:
            if n == 0 and not isinstance(new_info[3][0][0], int):
                new_info[3][0][0] = 2
                self.lines_got['p2'] += 1
            elif n == 1 and not isinstance(new_info[3][0][1], int):
                new_info[3][0][1] = 2
                self.lines_got['p2'] += 1
        elif n >= 2 and move in original_state[1][n]:
            for i in range(len(original_state[3])):
                if move_first in original_state[3][i] and i != 1:
                    c = i - 2
                elif move_first in original_state[3][i] and i == 1:
                    c = i - 1
            if not isinstance(new_info[3][c][-1], int):
                new_info[3][c][-1] = 2
                self.lines_got['p2'] += 1

    def helper_assignment3(self, n: int, new_info: list) -> None:
        """
        Helper function for assigning vertical lay line for player 1
        """

        if n <= self.game_size - 1 and \
                not isinstance(new_info[3][-1][n], int):
            new_info[3][-1][n] = 1
            self.lines_got['p1'] += 1
        elif n > self.game_size - 1:
            if not isinstance(new_info[3][-2][-1], int):
                new_info[3][-2][-1] = 1
                self.lines_got['p1'] += 1

    def helper_assignment4(self, n: int, new_info: list) -> None:
        """
        Helper function for assigning player 2 to the vertical lay line
        """
        if n <= self.game_size - 1 and \
                not isinstance(new_info[3][-1][n], int):
            new_info[3][-1][n] = 2
            self.lines_got['p2'] += 1
        elif n > self.game_size - 1:
            if not isinstance(new_info[3][-2][-1], int):
                new_info[3][-2][-1] = 2
                self.lines_got['p2'] += 1


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")

"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
import copy

# TODO: Adjust the type annotation as needed.

def interactive_strategy(game: 'StonehengeGame') -> str:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)

# TODO: Implement a recursive version of the minimax strategy.


def recursive_minimax_strategy(game) -> str:
    """
    Return a move that guarantees the highest score
    for a current player of the game
    Takes the possible moves(list) and evaluate
    all of the scores guaranteed by these
    """

    games = []
    for move in game.current_state.get_possible_moves():
        new_game = copy.deepcopy(game)
        new_game.current_state = new_game.current_state.make_move(move)
        if new_game.is_over(new_game.current_state) and \
                new_game.is_winner\
                            (game.current_state.get_current_player_name()):
            return move
        else:
            games.append(new_game)

    scores = []
    for items in games:
        player_score = final_state(items)
        scores.append(player_score)

    n = 0
    while n < len(scores) - 1:
        scores[n] *= -1
        n += 1

    highest = 0
    for i in range(len(scores)):
        if scores[i] > highest:
            highest = scores[i]

    moves_index = scores.index(highest)

    return game.current_state.get_possible_moves()[moves_index]


def final_state(game2) -> int:
    """
    Return the guaranteed score by the move recursively
    """

    if game2.is_over(game2.current_state):

        if not game2.is_winner(game2.current_state.get_current_player_name()):
            return -1
        elif game2.is_winner(game2.current_state.get_current_player_name()):
            return 1
        elif not game2.is_winner('p1') and not game2.is_winner('p2'):
            return 0
        return None

    else:
        games = []
        for move in game2.current_state.get_possible_moves():
            new_game = copy.deepcopy(game2)
            new_game.current_state = new_game.current_state.make_move(move)
            games.append(new_game)

        return max([(-1 * final_state(x)) for x in games])


# TODO: Implement an iterative version of the minimax strategy.


def iterative_minimax_strategy(game):
    """
    Return minimax that's not recursive
    """

    node_stack = Stack()
    game2 = copy.deepcopy(game)
    initial_node = Tree(game2)
    node_stack.add(initial_node)

    while not node_stack.is_empty():
        node = node_stack.remove()

        if node.value.is_over(node.value.current_state):
            if node.value.is_winner(
                    node.value.current_state.get_current_player_name()):
                node.score = 1
            elif not node.value.is_winner\
                        (node.value.current_state.get_current_player_name()):
                node.score = -1
            elif not node.value.is_winner('p1') and \
                    not node.value.is_winner('p2'):
                node.score = 0

        elif node.children == []:
            for move in node.value.current_state.get_possible_moves():
                item2 = copy.deepcopy(node.value)
                item2.current_state = item2.current_state.make_move(move)
                new_node = Tree(item2)
                node.children.append(new_node)
            node_stack.add(node)
            for child in node.children:
                node_stack.add(child)

        elif node.children != []:
            scores = []
            for child in node.children:
                scores.append(child.score * -1)
            node.score = max(scores)

    for i in range(len(initial_node.children)):
        if initial_node.children[i].score == -1 * initial_node.score:
            return game.current_state.get_possible_moves()[i]



class Stack:
    """ Last-in, first-out (LIFO) stack.
    """

    def __init__(self) -> None:
        """ Create a new, empty Stack self.

        >>> s = Stack()
        """
        self._contains = []

    def add(self, obj: object) -> None:
        """ Add object obj to top of Stack self.

        >>> s = Stack()
        >>> s.add(5)
        """
        self._contains.append(obj)

    def remove(self) -> object:
        """
        Remove and return top element of Stack self.

        Assume Stack self is not emp.

        >>> s = Stack()
        >>> s.add(5)
        >>> s.add(7)
        >>> s.remove()
        7
        """
        return self._contains.pop()

    def is_empty(self) -> bool:
        """
        Return whether Stack self is empty.

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.add(5)
        >>> s.is_empty()
        False
        """
        return len(self._contains) == 0


""" Tree class and functions
"""


class Tree:
    """
    A bare-bones Tree ADT that identifies the root with the entire tree.
    === Attributes ===
    @param object value: value of root node
    @param list[Tree|None] children: child nodes
    """
    def __init__(self, value=None, children=None, score=None):
        """
        Create Tree self with content value and 0 or more children
        @param Tree self: this tree
        @param object value: value contained in this tree
        @param list[Tree|None] children: possibly-empty list of children
        @rtype: None
        """
        self.value = value
        # copy children if not None
        # NEVER have a mutable default parameter...
        self.children = children[:] if children is not None else []
        self.score = score


if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")

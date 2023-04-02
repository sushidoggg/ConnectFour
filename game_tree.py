"""CSC111 Winter 2023 Project: Connect 4 (Game Tree)

Module Description
==================

This module contains a GameTree class of the game Connect 4
with a collection of functions defined under the class.
By reading the *docstring* of this file, you can gain insights into the
role and functionality of this class and functions
as well as how they contribute to this project as a whole.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the
Teaching Stream of CSC111 at the University of Toronto St. George campus.
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2023 Yige (Amanda) Wu, Sunyi (Alysa) Liu, Lecheng (Joyce) Qu, and Xi (Olivia) Yan.
Additionally, this file references a2_game_tree.py from CSC111 Assignment 2,
which is also Copyright (c) 2023 Mario Badr, David Liu, and Isaac Waller.
"""
from __future__ import annotations
from typing import Optional
from constant import GAME_START_MOVE, PLAYER_ONE
from connect_four import get_opposite_player


class GameTree:
    """A decision tree for ConnectFour column.

    Each node in the tree stores a possible ConnectFour column.

    Instance Attributes:
    - column: An int representing the current move (of either player_one or player_two),
    or '*' if this tree represents the start of a game.
    - player: Either PLAYER_ONE or PLAYER_TWO indicating which player is doing this move.
    - score: A float between 0.0 to 1.0 (inclusive), representing how this move is favorable to self.player.


    Representation Invariants:
    - column == GAME_START_MOVE or 0 <= self.column < 7
    - self.column == GAME_START_MOVE or self.player in {PLAYER_ONE, PLAYER_TWO}
    - 0.0 <= self.score <= 1.0
    # TODO: Introduce minimum score & average score
    # TODO: Player
    Current player will choose one of the possible moves in its subtress.
    """
    move_column: int | str
    initial_player: int
    current_player: Optional[int]
    score: int
    _subtrees: dict[int, GameTree]

    def __init__(self, move_column: str | int, initial_player: int, current_player: Optional[int],
                 score: Optional[int] = 0) -> None:
        """ Initialize a new game tree.

        Precondition:
        - column == GAME_START_MOVE or 0 <= column < 7
        - player in {PLAYER_ONE, PLAYER_TWO}
        """
        self.move_column = move_column
        self.initial_player = initial_player
        self.current_player = current_player
        self.score = score
        self._subtrees = {}

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of this game tree."""
        return list(self._subtrees.values())

    def get_subtree_by_column(self, column: int) -> Optional[GameTree]:
        """Return the subtree corresponding to the given column.

        Return None if no subtree corresponds to that column.
        """
        if column in self._subtrees:
            return self._subtrees[column]
        else:
            return None

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.

        You MAY change the implementation of this method (e.g. to display different instance attributes)
        as you work on this assignment.

        Preconditions:
            - depth >= 0
        """
        if self.current_player == PLAYER_ONE:
            turn_desc = "Player One"
        else:
            turn_desc = "Player Two"
        move_desc = f'{self.move_column}: {self.score} -> {turn_desc}\n'
        str_so_far = '  ' * depth + move_desc
        for subtree in self._subtrees.values():
            str_so_far += subtree._str_indented(depth + 1)
        return str_so_far

    def get_next_player(self) -> int:
        """Return the player who should move next."""
        if self.move_column == GAME_START_MOVE:
            return PLAYER_ONE
        else:
            return get_opposite_player(self.current_player)

    def __len__(self) -> int:
        """Return the number of items in this tree."""
        return 1 + sum(subtree.__len__() for subtree in self._subtrees.values())

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree."""
        self._subtrees[subtree.move_column] = subtree
        self.update_score()

    def update_score(self) -> None:
        """ Update the score for each new move.
        """
        if len(self._subtrees) == 0:
            # Do nothing when self is a leaf node
            return

        # Choose the maximum score among all subtrees and reverse it to be self's score.
        # TODO: Write a docstring and explain why
        if self.initial_player != self.current_player:
            max_subtree_score = max(subtree.score for subtree in self.get_subtrees())
            self.score = max_subtree_score
        else:
            min_subtree_score = min(subtree.score for subtree in self.get_subtrees())
            self.score = min_subtree_score


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'max-nested-blocks': 4,
        'extra-imports': ['__future__', 'typing', 'connect_four', 'constant'],
    })

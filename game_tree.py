"""
Module Description
==================
# TODO: Write a Docstring

Copyright and Usage Information
===============================
# TODO
"""

from __future__ import annotations
from typing import Optional
from connect_four import ConnectFour, UNOCCUPIED, PLAYER_ONE, PLAYER_TWO, GRID_WIDTH, GRID_HEIGHT

GAME_START_MOVE = "*"


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

    """
    column: int | str
    player: int
    score: float
    _subtrees: dict[int, GameTree]

    def __init__(self, column: str | int, player: int | None, score: Optional[float] = 0) -> None:
        """ Initialize a new game tree.

        Precondition:
        - column == GAME_START_MOVE or 0 <= column < 7
        - player in {PLAYER_ONE, PLAYER_TWO}
        """
        self.column = column
        self.player = player
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

    def get_next_player(self) -> int:
        """Return the player who should move next."""
        if self.column == GAME_START_MOVE:
            return PLAYER_ONE
        else:
            return self._get_opposite_player()

    def _get_opposite_player(self) -> int:
        """Return the opposite player of self.player.

        Since self.player is either 0 or 1 (PLAYER_ONE or PLAYER_TWO),
        we can use the x = 1 - x method to get the other possible value.
        """
        return 1 - self.player

    def __len__(self) -> int:
        """Return the number of items in this tree."""
        return 1 + sum(subtree.__len__() for subtree in self._subtrees.values())

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree."""
        self._subtrees[subtree.column] = subtree
        self._update_score()

    def _update_score(self) -> None:
        """ Update the score for each new move.
        """
        if len(self) == 1:
            # Do nothing when self is a leaf node
            return None
        else:
            # Choose the maximum score among all subtrees and reverse it to be self's score.
            # TODO: Write a docstring and explain why
            max_subtree_score = max(subtree.score for subtree in self.get_subtrees())
            self.score = 1 - max_subtree_score

    def insert_move_sequence(self, columns: list[str | int], score: Optional[int] = 0) -> None:
        """ Insert the given sequence of moves into this tree.

        """
        ...

    def insert_move_sequence_helper(self, columns: list[str | int], index: int,
                                    score: int = 0) -> None:
        """
        A helper funtion
        """
        if len(columns) <= index:
            return

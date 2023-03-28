from __future__ import annotations
from typing import Optional

GAME_START_MOVE = "*"


class GameTree:
    """A decision tree for ConnectFour column.

    Each node in the tree stores a possible ConnectFour column.

    Instance Attributes:
    - column: An int representing the current move (of either player_one or player_two),
    or '*' if this tree represents the start of a game
    - player: Either PLAYER_ONE or PLAYER_TWO indicating which player is doing this move.
    - score: An integer representing how this move is favorable to self.player.
    """
    column: int | str
    player: int
    score: int
    _subtrees: dict[int, GameTree]

    def __init__(self, column: str | int, player: int, score: Optional[int] = 0) -> None:
        """ Initialize a new game tree.

        Precondition:
        - player == PLAYER_ONE or player == PLAYER_TWO
        """
        self.column = column
        self.player = player
        self.score = score
        self._subtrees = {}

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of this game tree."""
        return list(self._subtrees.values())

    def find_subtree_by_column(self, column: int) -> Optional[GameTree]:
        """Return the subtree corresponding to the given column.

        Return None if no subtree corresponds to that column.
        """
        if column in self._subtrees:
            return self._subtrees[column]
        else:
            return None

    def is_player_one(self) -> bool:
        """Return whether the NEXT move should be made by player_one."""
        return self.column == GAME_START_MOVE

    def __len__(self) -> int:
        """Return the number of items in this tree."""
        return 1 + sum(subtree.__len__() for subtree in self._subtrees.values())

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree."""
        self._subtrees[subtree.column] = subtree
        self._update_score()

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

    def _update_score(self) -> None:
        """ Update the score for each new move.
        """
        ...

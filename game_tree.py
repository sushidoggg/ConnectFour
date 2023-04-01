"""CSC111 Winter 2023 Project: Connect 4 (Game Tree)

Module Description
==================

This module contains a GameTree class of the game Connect 4 with a collections of functions
defined under the class. By reading the *docstring* of this file, you can gain insights into the
role and functionality of this class and functions as well as how they contribute to this project as a whole.

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

import math
from typing import Optional
from connect_four import ConnectFour, UNOCCUPIED, PLAYER_ONE, PLAYER_TWO, GRID_WIDTH, GRID_HEIGHT
from player import score_position_for_alysa_AI, Player

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
    # TODO: Introduce minimum score & average score
    # TODO: Player

    """
    move_column: int | str
    initial_player: int
    current_player: Optional[int]
    score: float
    _subtrees: dict[int, GameTree]

    def __init__(self, move_column: str | int, initial_player: int, current_player: Optional[int],
                 score: Optional[float] = 0) -> None:
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
            return self._get_opposite_player()

    def _get_opposite_player(self) -> int:
        """Return the opposite player of self.player.

        Since self.player is either 0 or 1 (PLAYER_ONE or PLAYER_TWO),
        we can use the x = 1 - x method to get the other possible value.
        """
        return 1 - self.current_player

    def __len__(self) -> int:
        """Return the number of items in this tree."""
        return 1 + sum(subtree.__len__() for subtree in self._subtrees.values())

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree."""
        self._subtrees[subtree.move_column] = subtree
        self._update_score()

    def _update_score(self) -> None:
        """ Update the score for each new move.
        """
        if len(self._subtrees) == 0:
            # Do nothing when self is a leaf node
            return None

        # Choose the maximum score among all subtrees and reverse it to be self's score.
        # TODO: Write a docstring and explain why
        if self.initial_player == self.current_player:
            max_subtree_score = max(subtree.score for subtree in self.get_subtrees())
            self.score = - max_subtree_score
        else:
            min_subtree_score = min(subtree.score for subtree in self.get_subtrees())
            self.score = - min_subtree_score

    def get_average_subtree_score(self) -> float:
        """ Return the average of all subtree's score.

        Return self.score if there is no subtree
        """
        if len(self._subtrees) == 0:
            return self.score
        else:
            subtrees = self.get_subtrees()
            return sum(subtree.score for subtree in subtrees) / len(self._subtrees)

    def minimax(self, game: ConnectFour, depth: int, player_number: int, maxPlayer: bool) -> int:
        opponent_num = PLAYER_ONE
        if player_number == PLAYER_ONE:
            opponent_num = PLAYER_TWO
        if depth == 0 or self.get_subtrees() == []:
            if game.get_winner() is not None:
                if game.get_winner() == player_number:
                    return 10000
                elif game.get_winner() == opponent_num:
                    return -10000
                else: # No more valid moves
                    return 0
            else:
                return score_position_for_alysa_AI(game, player_number)
        if maxPlayer:
            value = int(-math.inf)
            for subtree in self.get_subtrees():
                copy_game = game.copy_and_record_player_move(subtree.move_column)
                new_score = max(value, subtree.minimax(copy_game, depth - 1, player_number, False))
                return new_score
        else:
            value = int(math.inf)
            for subtree in self.get_subtrees():
                copy_game = game.copy_and_record_player_move(subtree.move_column)
                new_score = min(value, subtree.minimax(copy_game, depth - 1, opponent_num, True))
                return new_score

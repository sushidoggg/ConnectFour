"""
Module Description
==================
# TODO: Write a Docstring

Copyright and Usage Information
===============================
# TODO
"""
from __future__ import annotations
import random
from typing import Optional
from game_tree import GameTree
from connect_four import ConnectFour, UNOCCUPIED, PLAYER_ONE, PLAYER_TWO, GRID_WIDTH, GRID_HEIGHT


class Player:
    """An abstract class representing a Player of Connect 4.

    Subclasses of this class will be created to implement different strategies for our Connect 4 AI player.

    Instance Attributes:
    - is_player_one: A boolean representing whether this player goes first.
    """
    is_player_one: bool

    def __init__(self, is_player_one: bool) -> None:
        """Initialize a player with a variable determining whether it goes first.
        """
        self.is_player_one = is_player_one

    def choose_column(self, game: ConnectFour) -> int:
        """ Return a chosen column of grid given the current game.
        """
        raise NotImplementedError


class RandomPlayer(Player):
    """ A player that performs randomly by selecting one of the possible moves at random.
    """
    def choose_column(self, game: ConnectFour) -> int:
        """ Return a randomly chosen column from all possible columns.
        """
        possible_columns = game.get_possible_columns()
        return random.choice(possible_columns)


class AIPlayer(Player):
    """ An abstract class representing an AI player of Connect 4.

    """
    _game_tree: GameTree | None

    def choose_column(self, game: ConnectFour) -> int:
        """ Return the column that is corresponding to the AI's move.
        """
        if game.player_one_moves == [] or self._game_tree is None:
            pass
        else:
            curr_move = game.get_sequence_moves()[-1]
            for subtree in self._game_tree.get_subtrees():
                if subtree.column == curr_move:
                    self._game_tree = subtree
                    break
                else:
                    self._game_tree = None

        if self._game_tree is None or self._game_tree.get_subtrees() == []:
            possible_columns = game.get_possible_columns()
            return random.choice(list(possible_columns))
        else:
            possible_answer_trees = self._game_tree.get_subtrees()

            possible_scores = [tree.score for tree in possible_answer_trees]
            max_score = max(possible_scores)
            max_score_trees = [t for t in possible_answer_trees if t.score == max_score]
            random_choice_max_score_tree = random.choice(max_score_trees)
            self._game_tree = random_choice_max_score_tree
            return random_choice_max_score_tree.move[1]

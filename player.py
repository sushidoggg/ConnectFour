"""CSC111 Winter 2023 Project: Connect 4 (Player)

Module Description
==================

This module contains a collection of Python classes and functions that
represent the game of Connect 4.
This file contains classes including Player, RandomPlayer and AIPlayer
with associated functions defined under each class.
By reading the *docstring* of this file, you can gain insights into the
role and functionality of these classes and functions
as well as how they contribute to this project as a whole.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the
Teaching Stream of CSC111 at the University of Toronto St. George campus.
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2023 Yige (Amanda) Wu, Sunyi (Alysa) Liu, Lecheng (Joyce) Qu, and Xi (Olivia) Yan.
Additionally, this file references a2_adversarial_wordle.py from CSC111 Assignment 2,
which is also Copyright (c) 2023 Mario Badr, David Liu, and Angela Zavaleta Bernuy.
"""

from __future__ import annotations
import random
from typing import Optional
from game_tree import GameTree, GAME_START_MOVE
from connect_four import ConnectFour, UNOCCUPIED, PLAYER_ONE, PLAYER_TWO, GRID_WIDTH, GRID_HEIGHT


class Player:
    """An abstract class representing a Player of Connect 4.

    Subclasses of this class will be created to implement different strategies for our Connect 4 AI player.

    Instance Attributes:
    - is_player_one: A boolean representing whether this player goes first.
    """
    player_num: int

    def __init__(self, player_num: int) -> None:
        """Initialize a player with a variable determining whether it goes first.
        """
        self.player_num = player_num

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
    _depth: int
    _game_tree: GameTree | None

    def __init__(self, player_num: int, _game_tree: Optional[GameTree], search_depth: int) -> None:
        """
        # TODO
        """
        Player.__init__(self, player_num)
        self._game_tree = _game_tree
        self._depth = search_depth

    def choose_column(self, game: ConnectFour) -> int:
        """ Return the column that is corresponding to the AI's move.
        """
        # FIXME: some ugly code style... edit later

        possible_columns = game.get_possible_columns()
        if len(possible_columns) == 1:
            return possible_columns[0]

        if self._game_tree is None:
            self._game_tree = generate_complete_tree_to_depth(GAME_START_MOVE, game, self._depth)
            # TODO: root move correct?

        last_move = game.get_last_move()
        if last_move is None:
            return random.choice(possible_columns)

        last_player, last_move_position = last_move
        last_move_column = last_move_position[0]
        if last_player == self.player_num:
            # last move is self, shouldn't reach this branch?
            return random.choice(possible_columns)

        # Recurse in last_player's tree
        self._game_tree = self._game_tree.get_subtree_by_column(last_move_column)
        subtrees = self._game_tree.get_subtrees()

        # Find the subtree with the largest 'minimum score'
        largest_minimum_score = max(subtree.minimum_score for subtree in subtrees)
        largest_minimum_score_subtrees = [subtree for subtree in subtrees
                                          if subtree.minimum_score == largest_minimum_score]
        if len(largest_minimum_score_subtrees) == 1:
            self._game_tree = largest_minimum_score_subtrees[0]

        else:
            # Break ties by finding the largest 'average score'
            largest_average_score = max(subtree.average_score for subtree in subtrees)
            largest_average_score_subtrees = [subtree for subtree in largest_minimum_score_subtrees
                                              if subtree.average_score == largest_average_score]
            if len(largest_average_score_subtrees) == 1:
                self._game_tree = largest_average_score_subtrees[0]

            else:
                # Choose a random one
                self._game_tree = random.choice(largest_average_score_subtrees)

        update_complete_tree_to_depth(self._game_tree, game, self._depth)
        return self._game_tree.column


def score_last_move(game_state: ConnectFour) -> float:
    """
    Score a move made by the next player in game_state.
    # TODO: add more docstring & preconditions
    """
    last_move = game_state.get_last_move()
    if last_move is None:
        return 0.0
    else:
        player, move_position = last_move

    attacking_score = _score_move_by_player(game_state, move_position, player)
    defending_score = _score_move_by_player(game_state, move_position, game_state.get_opposite_player())
    score = attacking_score + defending_score

    if score > 1.0:
        score = 1.0

    return score


def _score_move_by_player(game_state: ConnectFour, move_position: tuple[int, int], player: int) -> float:
    """
    Score a move made by the next player in game_state.
    # TODO: add more docstring & preconditions
    """
    connected_counts = game_state.get_connected_counts(move_position, player)

    if 4 in connected_counts:
        return 1.0

    score = 0.0
    if 3 in connected_counts:
        score += 0.3 * connected_counts[3]
    elif 2 in connected_counts:
        score += 0.1 * connected_counts[2]
    return score


def generate_complete_tree_to_depth(root_move: str | int, game_state: ConnectFour, d: int) -> GameTree:
    """ Returns a complete game tree to the depth d.

    Preconditions:
    - d >= 0
    - root_move == GAME_START_MOVE or 0 <= root_move < GRID_WIDTH
    # TODO: some more preconditions?
    """
    if root_move == GAME_START_MOVE:
        player = None
    else:
        player = game_state.get_current_player()

    if game_state.get_winner() is not None:
        # A winner already exists
        if game_state.get_winner() == player:
            return GameTree(root_move, player, score=1.0)
        else:
            # Shouldn't reach this branch
            return GameTree(root_move, player, score=-1.0)

    elif d == 0:
        # Reaches maximum search depth
        score = score_last_move(game_state)
        return GameTree(root_move, player, score=score)

    else:
        game_tree = GameTree(root_move, player, score=0.0)

        possible_columns = game_state.get_possible_columns()
        for column in possible_columns:
            new_game_state = game_state.copy_and_record_player_move(column)
            subtree = generate_complete_tree_to_depth(column, new_game_state, d - 1)
            game_tree.add_subtree(subtree)

        return game_tree


def update_complete_tree_to_depth(game_tree: GameTree, game_state: ConnectFour, d: int) -> None:
    """ Returns a complete game tree to the depth d.

    Preconditions:
    - d >= 0
    - root_move == GAME_START_MOVE or 0 <= root_move < GRID_WIDTH
    # TODO: some more preconditions?
    """
    if game_tree.get_subtrees():
        # No subtrees
        if game_state.get_winner() is None and d >= 0:

            possible_columns = game_state.get_possible_columns()
            for column in possible_columns:
                new_game_state = game_state.copy_and_record_player_move(column)
                subtree = generate_complete_tree_to_depth(column, new_game_state, d - 1)
                game_tree.add_subtree(subtree)

    else:
        # Recurse into next level
        for subtree in game_tree.get_subtrees():
            new_game_state = game_state.copy_and_record_player_move(subtree.column)
            update_complete_tree_to_depth(subtree, new_game_state, d - 1)


if __name__ == '__main__':
    connect_four = ConnectFour()

    first_player = input('Who goes first? Please type AI or Human:')
    if first_player == 'AI':
        AI_player = AIPlayer(PLAYER_ONE, None, 3)
        second_player = 'Human'
    else:
        AI_player = AIPlayer(PLAYER_TWO, None, 3)
        second_player = 'AI'

    current_player = first_player

    while connect_four.get_winner() is None:
        if current_player == 'Human':
            player_move = eval(input('Please choose column:'))
            connect_four.record_player_move(player_move)
            current_player = 'AI'
        else:
            print('AI is thinking...')
            connect_four.record_player_move(AI_player.choose_column(connect_four))
            current_player = 'Human'
        print(connect_four)

    if connect_four.get_winner() == PLAYER_ONE:
        print(first_player + ' wins!')
    else:
        print(second_player + ' wins!')

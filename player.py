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

import math
import random
from typing import Optional
from game_tree import GameTree, GAME_START_MOVE
from connect_four import ConnectFour, UNOCCUPIED, PLAYER_ONE, PLAYER_TWO, GRID_WIDTH, GRID_HEIGHT, get_opposite_player


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
    """
    # TODO
    """
    _game_tree: GameTree | None
    _depth: int

    def __init__(self, player_num: int, search_depth: int, game_tree: Optional[GameTree]) -> None:
        """
        # TODO
        """
        Player.__init__(self, player_num)

        if game_tree is not None:
            self._game_tree = game_tree
        else:
            self._game_tree = generate_complete_tree_to_depth(GAME_START_MOVE, ConnectFour(), search_depth,
                                                              self.player_num)

        self._depth = search_depth

    def choose_column(self, game: ConnectFour) -> int:
        """
        # TODO
        """
        # Recurse into last move's tree
        last_move = game.get_last_move()
        if last_move is None:
            assert self.player_num == PLAYER_ONE
            move_column = 3
            self._game_tree = self._game_tree.get_subtree_by_column(move_column)
            update_complete_tree_to_depth(self._game_tree, game.copy_and_record_player_move(move_column),
                                          self._depth, self.player_num)
            return move_column

        last_move_column = last_move[1][0]
        self._game_tree = self._game_tree.get_subtree_by_column(last_move_column)

        if self._game_tree is None:
            print('Empty game tree.')
            return random.choice(game.get_possible_columns())

        subtrees = self._game_tree.get_subtrees()

        if not subtrees:
            print('No subtrees.')
            return random.choice(game.get_possible_columns())

        # Always choose the subtree with maximum score
        max_score = max(subtree.score for subtree in subtrees)
        max_score_tree = [subtree for subtree in subtrees if subtree.score == max_score]

        move_column = random.choice(max_score_tree).move_column
        self._game_tree = self._game_tree.get_subtree_by_column(move_column)
        update_complete_tree_to_depth(self._game_tree, game.copy_and_record_player_move(move_column),
                                      self._depth, self.player_num)

        print(self._game_tree)

        return move_column


def generate_complete_tree_to_depth(root_move: str | int, game_state: ConnectFour, d: int,
                                    initial_player: int) -> GameTree:
    """ Returns a complete game tree to the depth d.

    Preconditions:
    - d >= 0
    - root_move == GAME_START_MOVE or 0 <= root_move < GRID_WIDTH
    # TODO: some more preconditions?
    """
    current_player = game_state.get_current_player()
    last_player = get_opposite_player(current_player)
    # Last player made the root_move. Current player will choose bewteen moves in subtrees

    if game_state.get_winner() is not None:
        # A winner already exists
        if game_state.get_winner() == initial_player:
            return GameTree(root_move, initial_player, last_player, score=1000)
        elif game_state.get_winner() == get_opposite_player(initial_player):
            return GameTree(root_move, initial_player, last_player, score=-500)
        else:
            # Game draws, so score = 0
            return GameTree(root_move, initial_player, last_player, score=0)

    elif d == 0:
        # Reaches maximum search depth, score the current situation
        score = score_game_state(game_state, get_opposite_player(last_player))
        return GameTree(root_move, initial_player, last_player, score=score)

    else:
        game_tree = GameTree(root_move, initial_player, last_player, score=0)

        possible_columns = game_state.get_possible_columns()
        for column in possible_columns:
            new_game_state = game_state.copy_and_record_player_move(column)
            subtree = generate_complete_tree_to_depth(column, new_game_state, d - 1, initial_player)
            game_tree.add_subtree(subtree)

        return game_tree


def update_complete_tree_to_depth(game_tree: GameTree, game_state: ConnectFour, d: int, initial_player: int) -> None:
    """ Returns a complete game tree to the depth d.

    Preconditions:
    - d >= 0
    - root_move == GAME_START_MOVE or 0 <= root_move < GRID_WIDTH
    # TODO: some more preconditions?
    """
    # FIXME: d == 0  should be treated differently, but how?

    if not game_tree.get_subtrees():
        # game_tree is a leaf
        if game_state.get_winner() is None and d >= 0:

            possible_columns = game_state.get_possible_columns()
            for column in possible_columns:
                new_game_state = game_state.copy_and_record_player_move(column)
                subtree = generate_complete_tree_to_depth(column, new_game_state, d - 1, initial_player)
                game_tree.add_subtree(subtree)

    else:
        # Recurse into next level
        for subtree in game_tree.get_subtrees():
            new_game_state = game_state.copy_and_record_player_move(subtree.move_column)
            update_complete_tree_to_depth(subtree, new_game_state, d - 1, initial_player)
        game_tree.update_score()


def score_game_state(game_state: ConnectFour, player: int) -> int:
    """
    # TODO
    """
    score_so_far = 0

    # Score center column
    center_array = [row[GRID_WIDTH // 2] for row in game_state.grid]
    center_count = center_array.count(player)
    score_so_far += 6 * center_count

    # Score horizontal
    for r in range(GRID_HEIGHT):
        row_array = game_state.grid[r]
        for c in range(GRID_WIDTH - 3):
            grid_slice = row_array[c: c + 4]
            score_so_far += _score_slice(grid_slice, player)

    # Score vertical
    for c in range(GRID_WIDTH):
        column_array = [row[c] for row in game_state.grid]
        for r in range(GRID_HEIGHT - 3):
            grid_slice = column_array[r: r + 4]
            score_so_far += _score_slice(grid_slice, player)

    # Score positive sloped diagonal
    for r in range(GRID_HEIGHT - 3):
        for c in range(GRID_WIDTH - 3):
            grid_slice = [game_state.grid[r + i][c + i] for i in range(4)]
            score_so_far += _score_slice(grid_slice, player)

    # Score negative sloped diagonal
    for r in range(GRID_HEIGHT - 3):
        for c in range(GRID_WIDTH - 3):
            grid_slice = [game_state.grid[r + 3 - i][c + i] for i in range(4)]
            score_so_far += _score_slice(grid_slice, player)

    return score_so_far


def _score_slice(grid_slice: list[int], player: int) -> int:
    """
    TODO
    """
    score_so_far = 0

    opponent = get_opposite_player(player)
    player_count, opponent_count = grid_slice.count(player), grid_slice.count(opponent)
    unoccupied_count = grid_slice.count(UNOCCUPIED)

    if player_count == 4:
        score_so_far += 100
    elif player_count == 3 and unoccupied_count == 1:
        score_so_far += 10
    elif player_count == 2 and unoccupied_count == 2:
        score_so_far += 5

    elif opponent_count == 3 and unoccupied_count == 1:
        score_so_far -= 80
    elif opponent_count == 2 and unoccupied_count == 2:
        score_so_far -= 8

    return score_so_far


def pick_best_column(game_state: ConnectFour, player_number: int) -> int:
    """
    # TODO: could make this a new AI class
    """
    best_score = -10000

    valid_columns = game_state.get_possible_columns()
    best_col = random.choice(valid_columns)

    for col in valid_columns:
        # position = connect_four.get_move_position_by_column(col)
        # row = position[0]
        new_game_state = game_state.copy_and_record_player_move(col)
        score = score_game_state(new_game_state, player_number)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


if __name__ == '__main__':
    connect_four = ConnectFour()

    first_player = input('Who goes first? Please type AI or Human:')
    if first_player == 'AI':
        AI_player = AIPlayer(PLAYER_ONE, 5, None)
        second_player = 'Human'
    else:
        AI_player = AIPlayer(PLAYER_TWO, 5, None)
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

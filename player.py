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
from typing import Optional
import random
from connect_four import ConnectFour, get_opposite_player
from game_tree import GameTree, GAME_START_MOVE
from constant import UNOCCUPIED, PLAYER_ONE, PLAYER_TWO, GRID_WIDTH, GRID_HEIGHT


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
        """ Return a chosen column of grid given the current game state.
        """
        raise NotImplementedError

    def hint_opponent(self, game: ConnectFour) -> int:
        """ Return a chosen column of grid given the current game state.
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

    def hint_opponent(self, game: ConnectFour) -> int:
        """ Return a randomly chosen column from all possible columns.
        """
        possible_columns = game.get_possible_columns()
        return random.choice(possible_columns)


class ScoringPlayer(Player):
    """
    # TODO
    """
    def choose_column(self, game: ConnectFour) -> int:
        """ Return a chosen column from all possible columns.
        """
        possible_columns = game.get_possible_columns()
        best_column_so_far = possible_columns[0]

        new_game = game.copy_and_record_player_move(best_column_so_far)
        best_score_so_far = score_game(new_game, self.player_num)

        for i in range(1, len(possible_columns)):
            column = possible_columns[i]
            new_game = game.copy_and_record_player_move(column)

            score = score_game(new_game, self.player_num)
            if score > best_score_so_far:
                best_score_so_far = score
                best_column_so_far = column

        return best_column_so_far

    def hint_opponent(self, game: ConnectFour) -> int:
        """ Return a chosen column from all possible columns.
        """
        opponent = get_opposite_player(self.player_num)
        possible_columns = game.get_possible_columns()
        best_column_so_far = possible_columns[0]

        new_game = game.copy_and_record_player_move(best_column_so_far)
        best_score_so_far = score_game(new_game, opponent)

        for i in range(1, len(possible_columns)):
            column = possible_columns[i]
            new_game = game.copy_and_record_player_move(column)

            score = score_game(new_game, opponent)
            if score > best_score_so_far:
                best_score_so_far = score
                best_column_so_far = column

        return best_column_so_far


class GreedyPlayer(Player):
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
            assert self.player_num == PLAYER_ONE    # TODO: make this a precondition
            move_column = GRID_WIDTH // 2
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
        # print(self._game_tree)

        return move_column

    def hint_opponent(self, game: ConnectFour) -> int:
        """ Return a column that the opponent should choose for their best interest according to self._game_tree
        """
        last_move = game.get_last_move()
        if last_move is None:
            return GRID_WIDTH // 2

        if self._game_tree is None:
            print('Empty game tree.')
            return random.choice(game.get_possible_columns())

        subtrees = self._game_tree.get_subtrees()

        if not subtrees:
            print('No subtrees.')
            return random.choice(game.get_possible_columns())

        subtrees = self._game_tree.get_subtrees()
        min_score = min(subtree.score for subtree in subtrees)
        min_score_tree = [subtree for subtree in subtrees if subtree.score == min_score]
        return random.choice(min_score_tree).move_column


def generate_complete_tree_to_depth(root_move: str | int, game: ConnectFour, d: int,
                                    initial_player: int) -> GameTree:
    """ Returns a complete game tree to the depth d.

    Preconditions:
    - d >= 0
    - root_move == GAME_START_MOVE or 0 <= root_move < GRID_WIDTH
    # TODO: some more preconditions?
    """
    current_player = game.get_current_player()
    last_player = get_opposite_player(current_player)
    # Last player made the root_move. Current player will choose bewteen moves in subtrees

    if game.get_winner() is not None:
        # A winner already exists
        if game.get_winner() == initial_player:
            return GameTree(root_move, initial_player, last_player, score=1000)
        elif game.get_winner() == get_opposite_player(initial_player):
            return GameTree(root_move, initial_player, last_player, score=-500)
        else:
            # Game draws, so score = 0
            return GameTree(root_move, initial_player, last_player, score=0)

    elif d == 0:
        # Reaches maximum search depth, score the current situation
        score = score_game(game, initial_player)
        return GameTree(root_move, initial_player, last_player, score=score)

    else:
        game_tree = GameTree(root_move, initial_player, last_player, score=0)

        possible_columns = game.get_possible_columns()
        for column in possible_columns:
            new_game = game.copy_and_record_player_move(column)
            subtree = generate_complete_tree_to_depth(column, new_game, d - 1, initial_player)
            game_tree.add_subtree(subtree)

        return game_tree


def update_complete_tree_to_depth(game_tree: GameTree, game: ConnectFour, d: int, initial_player: int) -> None:
    """ Returns a complete game tree to the depth d.

    Preconditions:
    - d >= 0
    - root_move == GAME_START_MOVE or 0 <= root_move < GRID_WIDTH
    # TODO: some more preconditions?
    """
    # FIXME: d == 0  should be treated differently, but how?

    if not game_tree.get_subtrees():
        # game_tree is a leaf
        if game.get_winner() is not None:
            if game.get_winner() == initial_player:
                game_tree.score = 1000
            elif game.get_winner() == get_opposite_player(initial_player):
                game_tree.score = -500
            else:
                # Game draws, so score = 0
                game_tree.score = 0

        elif d == 0:
            game_tree.score = score_game(game, initial_player)

        elif d > 0:
            possible_columns = game.get_possible_columns()
            for column in possible_columns:
                new_game = game.copy_and_record_player_move(column)
                subtree = generate_complete_tree_to_depth(column, new_game, d - 1, initial_player)
                game_tree.add_subtree(subtree)

    else:
        # Recurse into next level
        for subtree in game_tree.get_subtrees():
            new_game = game.copy_and_record_player_move(subtree.move_column)
            update_complete_tree_to_depth(subtree, new_game, d - 1, initial_player)
        game_tree.update_score()


def score_game(game: ConnectFour, player: int) -> int:
    """
    # TODO
    """
    score_so_far = 0

    # Score center column
    center_array = [row[GRID_WIDTH // 2] for row in game.grid]
    center_count = center_array.count(player)
    score_so_far += 6 * center_count

    # Score horizontal
    for r in range(GRID_HEIGHT):
        row_array = game.grid[r]
        for c in range(GRID_WIDTH - 3):
            grid_slice = row_array[c: c + 4]
            score_so_far += _score_slice(grid_slice, player)

    # Score vertical
    for c in range(GRID_WIDTH):
        column_array = [row[c] for row in game.grid]
        for r in range(GRID_HEIGHT - 3):
            grid_slice = column_array[r: r + 4]
            score_so_far += _score_slice(grid_slice, player)

    # Score positive sloped diagonal
    for r in range(GRID_HEIGHT - 3):
        for c in range(GRID_WIDTH - 3):
            grid_slice = [game.grid[r + i][c + i] for i in range(4)]
            score_so_far += _score_slice(grid_slice, player)

    # Score negative sloped diagonal
    for r in range(GRID_HEIGHT - 3):
        for c in range(GRID_WIDTH - 3):
            grid_slice = [game.grid[r + 3 - i][c + i] for i in range(4)]
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
        score_so_far += 80
    elif player_count == 2 and unoccupied_count == 2:
        score_so_far += 5
    elif opponent_count == 4:
        score_so_far -= 90
    elif opponent_count == 3 and unoccupied_count == 1:
        score_so_far -= 60
    elif opponent_count == 2 and unoccupied_count == 2:
        score_so_far -= 8

    return score_so_far


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'max-nested-blocks': 4,
    #     'extra-imports': ['__future__', 'typing', 'random', 'connect_four', 'game_tree', 'constant'],
    # })
    #

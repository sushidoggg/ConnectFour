"""CSC111 Winter 2023 Project: Connect 4 (Player)

Module Description
==================

This module contains a collection of Python classes and functions that
represent the game of Connect 4.
This file contains classes including Player, RandomPlayer, ScoringPlayer, and GreedyPlayer
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
from constant import GRID_WIDTH, GRID_HEIGHT


class Player:
    """An abstract class representing a Player of Connect 4.

    Subclasses of this class will be created to implement different strategies for our Connect 4 AI player.

    Instance Attributes:
        - player_num: An int representing whether this player goes first or second.

    Representation Invariants:
        - player_num in {PLAYER_ONE, PLAYER_TWO}
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

    def copy(self) -> Player:
        """ Return a copy of the current player.
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

    def copy(self) -> Player:
        """ Return a copy of self.
        """
        return RandomPlayer(self.player_num)


class ScoringPlayer(Player):
    """ A Scoring AI Player that makes move by scoring its possible moves and choose the move with the largest score.

    The scoring player evaluates only one next step. In principle, it is similar to a GreedyPlayer with depth 1.
    """

    def choose_column(self, game: ConnectFour) -> int:
        """ Return a chosen column from all possible columns with the maximum score.

        Preconditions:
            - game.get_last_move() is not none or self.player_num == PLAYER_ONE
            - game.get_winner() is None
            - game.get_current_player() == self.player_num
        """
        possible_columns = game.get_possible_columns()
        best_column_so_far = possible_columns[0]

        new_game = game.copy_and_record_player_move(best_column_so_far)
        best_score_so_far = score_game(new_game, self.player_num, True)

        for i in range(1, len(possible_columns)):
            column = possible_columns[i]
            new_game = game.copy_and_record_player_move(column)

            score = score_game(new_game, self.player_num, True)
            if score > best_score_so_far:
                best_score_so_far = score
                best_column_so_far = column

        return best_column_so_far

    def hint_opponent(self, game: ConnectFour) -> int:
        """ Return a chosen column from all possible columns with the maximum score for the opponent.

        This is very similar to choose_column, but we are scoring for the opponent.

        Preconditions:
            - game.get_last_move() is not none or self.player_num == PLAYER_TWO
            - game.get_winner() is None
            - game.get_current_player() == self.player_num
        """
        opponent = get_opposite_player(self.player_num)
        possible_columns = game.get_possible_columns()
        best_column_so_far = possible_columns[0]

        new_game = game.copy_and_record_player_move(best_column_so_far)
        best_score_so_far = score_game(new_game, opponent, True)

        for i in range(1, len(possible_columns)):
            column = possible_columns[i]
            new_game = game.copy_and_record_player_move(column)

            score = score_game(new_game, opponent, True)
            if score > best_score_so_far:
                best_score_so_far = score
                best_column_so_far = column

        return best_column_so_far

    def copy(self) -> Player:
        """Return a copy of self."""
        return ScoringPlayer(self.player_num)


class GreedyPlayer(Player):
    """ A Greedy AI Player that makes move based on its game tree.

    Private Instance Attributes:
        - _depth: An integer representing the depth of the decision tree.
        - _game_tree: A GameTree object representing the decision tree of the greedy player.

    Representation Invariant:
        - self._depth > 0
    """
    _depth: int
    _game_tree: GameTree | None

    def __init__(self, player_num: int, search_depth: int, game_tree: Optional[GameTree]) -> None:
        """Initiate a GreedyPlayer with given player number, search depth and game_tree.

        Generate a new game tree if game_tree is None.

        Preconditions:
            - player_num in {PLAYER_ONE, PLAYER_TWO}
            - search_depth > 0
        """
        Player.__init__(self, player_num)

        if game_tree is not None:
            self._game_tree = game_tree
        else:
            self._game_tree = generate_complete_tree_to_depth(GAME_START_MOVE, ConnectFour(), search_depth,
                                                              self.player_num)

        self._depth = search_depth

    def choose_column(self, game: ConnectFour) -> int:
        """ Choose a column with maximum score based on the given game and game tree.
        Recurse in to the chosen game tree branch.

        Choose a random possible column if either game tree is None or game tree has no subtree.

        Preconditions:
            - game.get_last_move() is not none or self.player_num == PLAYER_ONE
            - game.get_winner() is None
            - game.get_current_player() == self.player_num
        """

        last_move = game.get_last_move()

        # Always choose the central column when making the first step of the whole game.
        if last_move is None:
            move_column = GRID_WIDTH // 2
            self._recurse_into_tree(move_column, game)
            return move_column

        # Recurse into a subtree based on the last move of the game (the opponent's move).
        last_move_column = last_move[1][0]
        self._game_tree = self._game_tree.get_subtree_by_column(last_move_column)

        # Make random choices if either game tree is None or game tree has no subtree.
        if self._game_tree is None:
            return random.choice(game.get_possible_columns())

        subtrees = self._game_tree.get_subtrees()

        if not subtrees:
            return random.choice(game.get_possible_columns())

        # Always choose the subtree with maximum score
        max_score = max(subtree.score for subtree in subtrees)
        max_score_tree = [subtree for subtree in subtrees if subtree.score == max_score]

        move_column = random.choice(max_score_tree).move_column
        self._recurse_into_tree(move_column, game)
        return move_column

    def _recurse_into_tree(self, move_column: int, game: ConnectFour) -> None:
        """ Recurse game tree into the given column. Update the game tree to maintain its depth, so that
        the following moves can still be based a tree with self._depth.

        Preconditions:
            - move_column in game.get_possible_columns()
        """
        self._game_tree = self._game_tree.get_subtree_by_column(move_column)
        new_game = game.copy_and_record_player_move(move_column)
        update_complete_tree_to_depth(self._game_tree, new_game, self._depth, self.player_num)

    def hint_opponent(self, game: ConnectFour) -> int:
        """ Return a column that the opponent should choose for their best interest according to self._game_tree.

        Preconditions:
            - game.get_last_move() is not none or self.player_num == PLAYER_TWO
            - game.get_winner() is None
            - game.get_current_player() == self.player_num
        """
        last_move = game.get_last_move()
        if last_move is None:
            return GRID_WIDTH // 2

        if self._game_tree is None:
            return random.choice(game.get_possible_columns())

        subtrees = self._game_tree.get_subtrees()

        if not subtrees:
            return random.choice(game.get_possible_columns())

        # Always choose the subtree with minimum score
        subtrees = self._game_tree.get_subtrees()
        min_score = min(subtree.score for subtree in subtrees)
        min_score_tree = [subtree for subtree in subtrees if subtree.score == min_score]
        return random.choice(min_score_tree).move_column

    def copy(self) -> Player:
        """
        Return a copy of self with the same search depth and game tree.
        """
        return GreedyPlayer(self.player_num, self._depth, self._game_tree)


def generate_complete_tree_to_depth(root_move: str | int, game: ConnectFour, d: int,
                                    initial_player: int) -> GameTree:
    """ Generate a complete game tree to the depth d recursively.

    Since generating a complete tree to the maximum possible depth is very time and space consuming, we
    will stop at a certain depth, and evaluate the game state at the leaf node by a scoring function.

    Base case:
    If the game is over, return a game tree whose score has been evaluated based on the winner.
    If the maximum depth is reached, return game tree whose score has been evaluated based on the score_game fucntion.

    Resursive steps:
    Create an empty game tree. For all possible game moves, create its associated subtree to depth d - 1,
    and add to the empty game tree's subtrees.

    Preconditions:
        - d >= 0
        - root_move == GAME_START_MOVE or 0 <= root_move < GRID_WIDTH
        - len(game.player_one_moves) == 0 or root_move != GAME_START_MOVE
        - initial_player in {PLAYER_ONE, PLAYER_TWO}
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
        if initial_player == last_player:
            score = score_game(game, initial_player, False)
        else:
            score = score_game(game, initial_player, True)
        return GameTree(root_move, initial_player, last_player, score=score)

    else:
        # Recursive steps
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
        - len(game.player_one_moves) == 0 or root_move != GAME_START_MOVE
        - initial_player in {PLAYER_ONE, PLAYER_TWO}
    """

    if not game_tree.get_subtrees():
        # game_tree is a leaf
        current_player = game.get_current_player()
        last_player = get_opposite_player(current_player)

        if game.get_winner() is not None:
            if game.get_winner() == initial_player:
                game_tree.score = 1000
            elif game.get_winner() == get_opposite_player(initial_player):
                game_tree.score = -500
            else:
                # Game draws, so score = 0
                game_tree.score = 0

        elif d == 0:
            if initial_player == last_player:
                game_tree.score = score_game(game, initial_player, False)
            else:
                game_tree.score = score_game(game, initial_player, True)

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


def score_game(game: ConnectFour, player: int, is_moving_next: bool) -> int:
    """ Score how favorable the game state is to this player, given whether he is moving next.

    is_moving_next means whether this player will make the next move. This variable is included
    because this function can be called when player is moving next or when his opponent is moving next.

    This function evaluates the whole game grid by iterating through all possible 4-in-a-row slices in
    horizontal, vertical, and two diagonal. The total score returned is the sum of the score of each slice.

    The center column is also scored and added to the total score since taking up the central column
    is very crucial to winning the game. This is because any horizontal or slanted 4 connected discs
    on the grid must have at least one disc in the central column.

    Preconditions:
        - player in {PLAYER_ONE, PLAYER_TWO}
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
            score_so_far += _score_slice(grid_slice, player, is_moving_next)

    # Score vertical
    for c in range(GRID_WIDTH):
        column_array = [row[c] for row in game.grid]
        for r in range(GRID_HEIGHT - 3):
            grid_slice = column_array[r: r + 4]
            score_so_far += _score_slice(grid_slice, player, is_moving_next)

    # Score positive sloped diagonal
    for r in range(GRID_HEIGHT - 3):
        for c in range(GRID_WIDTH - 3):
            grid_slice = [game.grid[r + i][c + i] for i in range(4)]
            score_so_far += _score_slice(grid_slice, player, is_moving_next)

    # Score negative sloped diagonal
    for r in range(GRID_HEIGHT - 3):
        for c in range(GRID_WIDTH - 3):
            grid_slice = [game.grid[r + 3 - i][c + i] for i in range(4)]
            score_so_far += _score_slice(grid_slice, player, is_moving_next)

    return score_so_far


def _score_slice(grid_slice: list[int], player: int, player_go_next: bool) -> int:
    """ Score a slice of four discs with respective to the player, given whether he is moving next.

    If the slice contains both player's discs and opponent's discs, we give it a 0, because
    both parties can't connect four in this slice.

    Otherwise, we give positive scores if player is occupying this slice, and negative scores if opponent is
    occupying this slice. We give a higher score if more discs are connected. The specific score scheme is
    stored in the four lists.

    Based on whether player goes next, we value player and opponent's discs differently. If the player
    goes next, we think attacking is more important. Thus, the absolute value of go_next_player_score is larger
    than that of go_next_opponent_score. This means that the player's connected discs influence the
    overall score to a larger extent. If the opponent goes next, we think defending is more important. The
    scoring scheme is thus opposite to the other case.

    Preconditions:
        - len(grid_slice) = 4
        - player in {PLAYER_ONE, PLAYER_TWO}
    """

    opponent = get_opposite_player(player)
    player_count, opponent_count = grid_slice.count(player), grid_slice.count(opponent)

    if player_count != 0 and opponent_count != 0:
        # The grid contains both player's disc and opponent's disc
        return 0

    # Represents the given score if the party hax 0/1/2/3/4 connected discs.
    go_next_player_score = [0, 0, 8, 90, 100]
    go_next_opponent_score = [0, 0, -5, -60, -100]
    not_next_player_score = [0, 0, 5, 60, 100]
    not_next_opponent_score = [0, 0, -8, -90, 100]

    if player_go_next:
        return go_next_player_score[player_count] + go_next_opponent_score[opponent_count]
    else:
        return not_next_player_score[player_count] + not_next_opponent_score[opponent_count]


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'max-nested-blocks': 4,
        'extra-imports': ['__future__', 'typing', 'random', 'connect_four', 'game_tree', 'constant'],
    })

"""CSC111 Winter 2023 Project: Connect 4

Module Description
==================

This module contains a main class ConnectFour that represents the game of Connect 4
with a collection of Python functions defined under this class.
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
Additionally, this file references a2_adversarial_wordle.py from CSC111 Assignment 2,
which is also Copyright (c) 2023 Mario Badr, David Liu, and Angela Zavaleta Bernuy.
"""
from __future__ import annotations
from typing import Optional

from constant import UNOCCUPIED, PLAYER_ONE, PLAYER_TWO, GRID_WIDTH, GRID_HEIGHT, ORIENTATIONS


class ConnectFour:
    """
    Representing state of game of a ConnectFour game.

    Instance Attributes:
    - grid
        A list of list of int that forms a grid of size 7x6 to represent the current gaming board.
        In each spot of the grid, it is either filled with UNOCCUPIED, PLAYER_ONE, or PLAYER_TWO.
    - player_one_moves: A list of tuples representing moves made by the first player.
    - player_two_moves: A list of tuples representing moves made by the second player.

    Private Instance Attributes:
    - _possible_columns: A list of int representing valid columns that players can choose from.
    - _winner: An int representing the winner of the game. None if the game has not ended yet.

    Representation Invariants:
    - len(self.grid) == GRID_HEIGHT and all(len(row) == GRID_WIDTH for row in self.grid)
    - all(self.grid[y][x] in {UNOCCUPIED, PLAYER_ONE, PLAYER_ONE} for y in range(GRID_HEIGHT)\
     for x in range(GRID_WIDTH))
    - all(0 <= move[0] < GRID_WIDTH and 0 <= move[1] < GRID_HEIGHT for move in self.player_one_moves)
    - all(0 <= move[0] < GRID_WIDTH and 0 <= move[1] < GRID_HEIGHT for move in self.player_two_moves)
    - all(0 <= move < GRID_WIDTH for move in self._possible_columns)
    - self._winner in {None, UNOCCUPIED, PLAYER_ONE, PLAYER_TWO}
    """
    grid: list[list[int]]
    player_one_moves: list[tuple[int, int]]
    player_two_moves: list[tuple[int, int]]
    _possible_columns: list[int]
    _winner: int | None

    def __init__(self) -> None:
        """Initialize a new Connect 4 game."""
        self.grid = [[UNOCCUPIED] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.player_one_moves = []
        self.player_two_moves = []
        self._possible_columns = [i for i in range(GRID_WIDTH)]
        self._winner = None

    def __str__(self) -> str:
        """
        Return a string representation of the ConnectFour game.

        We used the following symbols to represent the grid's state:
        UNOCCUPIED: -, PLAYER_ONE: O, PLAYER_TWO: X

        >>> connect_four = ConnectFour()
        >>> connect_four.record_player_move(3)
        >>> connect_four.record_player_move(4)
        >>> connect_four.record_player_move(4)
        >>> print(connect_four)
        |   | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
        | 5 | - | - | - | - | - | - | - |
        | 4 | - | - | - | - | - | - | - |
        | 3 | - | - | - | - | - | - | - |
        | 2 | - | - | - | - | - | - | - |
        | 1 | - | - | - | - | O | - | - |
        | 0 | - | - | - | O | X | - | - |

        """
        string = '|   | 0 | 1 | 2 | 3 | 4 | 5 | 6 |'
        for y in range(GRID_HEIGHT - 1, -1, -1):
            string += '\n| ' + str(y) + ' |'
            for x in range(GRID_WIDTH):
                if self.grid[y][x] == UNOCCUPIED:
                    string += ' - |'
                elif self.grid[y][x] == PLAYER_ONE:
                    string += ' O |'
                elif self.grid[y][x] == PLAYER_TWO:
                    string += ' X |'
        return string

    def get_current_player(self) -> int:
        """ Retern which player should make the next move.
        """
        if len(self.player_one_moves) == len(self.player_two_moves):
            # player_one should make the next move
            return PLAYER_ONE
        return PLAYER_TWO

    def record_player_move(self, move_column: int) -> None:
        """
        Record the given move made by the current player.

        Preconditions:
        - move_column in self._possible_columns

        >>> connect_four = ConnectFour()
        >>> connect_four.record_player_move(3)
        >>> connect_four.record_player_move(3)
        >>> connect_four.grid[0][3] == PLAYER_ONE
        True
        >>> connect_four.grid[1][3] == PLAYER_TWO
        True
        >>> connect_four.player_one_moves
        [(3, 0)]
        >>> connect_four.player_two_moves
        [(3, 1)]
        """
        # Get an (x, y) representation of the move.
        move_position = self.get_move_position_by_column(move_column)

        self._update_grid(move_position)
        self._update_possible_columns()
        self._update_winner(move_position)

        # These lines must be at the end because we determine the current player by comparing
        # the length of self.player_one_moves and self.player_two_moves.
        if self.get_current_player() == PLAYER_ONE:
            self.player_one_moves.append(move_position)
        else:
            self.player_two_moves.append(move_position)

    def _update_grid(self, move_position: tuple[int, int]) -> None:
        """ Update self.grid by inserting the current player's number into the grid according to move_position.

        Preconditions:
        - move_position[0] in self._possible_columns
        - move_position[1] == 0 or move[move_position[1] - 1][move_position[0]] != UNOCCUPIED
        """
        self.grid[move_position[1]][move_position[0]] = self.get_current_player()

    def _update_possible_columns(self) -> None:
        """
        Update the possible columns from which the players can choose.

        A column is considered to be a possible column if it is not filled up to the top.
        """
        self._possible_columns = []
        for x in range(GRID_WIDTH):
            if any(self.grid[y][x] == UNOCCUPIED for y in range(GRID_HEIGHT)):
                self._possible_columns.append(x)

    def _update_winner(self, move_position: tuple[int, int]) -> None:
        """
        Update self._winner by checking if current player's move at move_position would result in him winning.

        Set self._winner to be UNOCCUPIED if there's a draw (when there is no possible columns).

        Preconditions:
        - move_position[0] in self._possible_columns
        - move_position[1] == 0 or move[move_position[1] - 1][move_position[0]] != UNOCCUPIED
        """
        if self._winner is not None:
            return

        if not self._possible_columns:
            # Update self._winner when game draws
            self._winner = UNOCCUPIED

        current_player = self.get_current_player()
        if self._is_four_connected(move_position):
            self._winner = current_player

    def _is_four_connected(self, move_position: tuple[int, int]) -> bool:
        """ Checks whether player placing a move at this position will result in four connected discs.

        Preconditions:
        - move_position[0] in self._possible_columns
        - move_position[1] == 0 or move[move_position[1] - 1][move_position[0]] != UNOCCUPIED
        """
        player = self.get_current_player()

        for i in range(4):
            # Check for four orientations (horizontal, vertical, two diagonal) for connected discs.
            orientation_x, orientation_y = ORIENTATIONS[i]
            connected_so_far = 1  # a disc is at least connected to itself

            # Check for opposite directions. For example, left & right are two
            # opposite directions for the horizontal orientation.
            for direction_x, direction_y in ((orientation_x, orientation_y), (-orientation_x, -orientation_y)):

                pos_x, pos_y = move_position[0] + direction_x, move_position[1] + direction_y

                while 0 <= pos_x < GRID_WIDTH and 0 <= pos_y < GRID_HEIGHT \
                        and self.grid[pos_y][pos_x] == player and connected_so_far < 4:

                    connected_so_far += 1
                    # Update the next position to check
                    pos_x += direction_x
                    pos_y += direction_y

                if connected_so_far >= 4:
                    return True
        return False

    def copy_and_record_player_move(self, move_column: int) -> ConnectFour:
        """ Return a copy of this game state with the given move recorded.

        Preconditions:
        - move_column in self._possible_columns
        """
        new_game = self._copy()
        new_game.record_player_move(move_column)
        return new_game

    def _copy(self) -> ConnectFour:
        """ Return a copy of this game state."""
        new_game = ConnectFour()
        new_game.grid = [[self.grid[y][x] for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
        new_game.player_one_moves.extend(self.player_one_moves)
        new_game.player_two_moves.extend(self.player_two_moves)
        new_game._possible_columns.extend(self._possible_columns)
        new_game._winner = self._winner
        return new_game

    def get_move_position_by_column(self, move_column: int) -> tuple[int, int]:
        """ Find the position of a disc in the grid if it is placed at move_column.

        The returned tuple is in the form of (x, y) where x is the horizontal position and y is
        the vertical position. In other words, self.grid[y][x] is the corresponding position.

        The purpose of distinguishing between move_position and move_column is to make sure that
        players don't make invalid moves. Players only need choose a column in each move and the disc
        will "fall" automatically. However, in order to store it in our grid, we need a (x, y) coordinate,
        hence we need a function to convert.

        Precondition:
        - move_column in self._possible_columns
        """
        for y in range(GRID_HEIGHT):
            if self.grid[y][move_column] == UNOCCUPIED:
                return (move_column, y)

    def get_last_move(self) -> tuple[int, tuple[int, int]] | None:
        """ Get the last move of the state.

        The returned tuple is in the form of (player, move_position), where player is either
        PLAYER_ONE or PLAYER_TWO, and move_position is a tuple (x, y) coordinates.

        Return None if no move has been made.
        """
        if len(self.player_one_moves) == 0:
            return None
        elif len(self.player_one_moves) == len(self.player_two_moves):
            return (PLAYER_TWO, self.player_two_moves[-1])
        else:
            return (PLAYER_ONE, self.player_one_moves[-1])

    def get_possible_columns(self) -> list[int]:
        """ Return the possible moves for the current game state, or [] if a player has won the game.
        """
        if self.get_winner() is None:
            return self._possible_columns
        else:
            return []

    def get_winner(self) -> Optional[int]:
        """Return the winner of the game (either PLAYER_ONE or PLAYER_TWO).

        Return None if the game is not over.

        Return UNOCCUPIED if there is a draw game.
        """
        return self._winner


def get_opposite_player(player: int) -> int:
    """
    Return the opposite player.

    Since the current player is either 0 or 1 (PLAYER_ONE or PLAYER_TWO),
    we can use the x = 1 - x method to get the other possible value.

    Preconditions:
    - player in {PLAYER_ONE, PLAYER_TWO}
    """
    return 1 - player


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

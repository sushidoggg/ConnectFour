"""errr"""

from future import annotations
UNOCCUPIED, PLAYER_ONE, PLAYER_TWO = -1, 0, 1
GRID_WIDTH, GRID_HEIGHT = 7, 6


class ConnectFour:
    """
    Representing state of game of a ConnectFour game.

    Instance Attributes:
    - grid: list of list of int representing the current gaming grid.
    - player_one_moves: list of tuples representing moves made by the first player.
    - player_two_moves: list of tuples representing moves made by the second player.

    Representation Invariants:
    - len(grid) == 6 and all(len(row) == 7 for row in grid)
    - all(move[0] < 7 and move[1] < 6 for move in player_one_moves)
    - all(move[0] < 7 and move[1] < 6 for move in player_two_moves)
    """
    grid: list[list[int]]
    player_one_moves: list[tuple[int]]
    player_two_moves: list[tuple[int]]
    _possible_columns: list[int]

    def __init__(self) -> None:
        """Initialize a new Connect 4 game"""
        self.grid = [[UNOCCUPIED] * GRID_WIDTH for y in range(GRID_HEIGHT)]
        self.player_one_moves = []
        self.player_two_moves = []
        self._possible_columns = [i for i in range (GRID_WIDTH)]

    def is_player_one_turn(self) -> bool:
        """ Retern a boolean that represents whether or not it is the first player's turn.
        """
        return len(self.player_one_moves) == len(self.player_two_moves)

    def record_player_move(self, move_column: int) -> None:
        """
        Record the given move made by the current player.

        Preconditions:
        - move in self._possible_columns
        """
        tuple_move = self.get_tuple_by_col(move_column)
        if self.is_player_one_turn():
            self.player_one_moves.append(tuple_move)
        else:
            self.player_two_moves.append(tuple_move)
        self._update_possible_column()
        self._update_grid(tuple_move)

    def _update_grid(self, tuple_move: tuple[int]) -> None:
        """
        Update the current grid.
        """
        if self.is_player_one_turn():
            self.grid[tuple_move[0]][tuple_move[1]] = 0
        else:
            self.grid[tuple_move[0]][tuple_move[1]] = 1


    def get_tuple_by_col(self, move_column: int) -> tuple[int]:
        """
        Return the place in grid as a tuple of int.

        Precondition:
        - move_column in self._possible_column
        """
        for i in range(GRID_HEIGHT):
            if self.grid[i][move_column] == UNOCCUPIED:
                return (i, move_column)

    def _update_possible_column(self) -> None:
        """
        Update the possible columns with empty spaces which the next move can choose from.
        """
        self._possible_columns = []
        for x in range(GRID_WIDTH):
            if any(self.grid[y][x] == UNOCCUPIED for y in range(GRID_HEIGHT)):
                self._possible_columns.append(x)

    def get_possible_column(self) -> list[tuple]:
        """ Return the possible moves for the current game state, or [] if a player has won the game.
        """
        if self.get_winner() is None:
            return self._possible_columns
        else:
            return []

    def get_winner(self) -> Optional[str]:
        """Return the winner of the game ('Player 1' or 'Player 2').

        Return None if the game is not over.
        """
        if len(self.player_two_moves) == 0 or len(self.player_one_moves) == 0:
            return None
        elif ...:
            ...
        # TODO

    def get_sequence_moves(self) -> list[tuple[int]]:
        """
        Return the move sequence made in this game.
        """
        moves_so_far = []
        for i in range(len(self.player_one_moves)):
            moves_so_far.append(self.player_one_moves[i])
            if i < len(self.player_two_moves):
                moves_so_far.append(self.player_two_moves[i])
        return moves_so_far

def is_four_connected(grid: list[list[int]], move: tuple[int]) -> bool:

    return ...


class Player:
    """An abstract class representing a Player of Connect 4.

    This class can be subclassed to implement different strategies for the Connect 4 player.

    Instance Attributes:
    - is_player_one: A boolean representing whether or not this player goes first.
    """
    is_player_one: bool
    _game_tree: Optional[GameTree]

    def __init__(self, is_player_one: bool) -> None:
        "Initialize a player with a variable determining whether it goes first."
        self.is_player_one = is_player_one

    def choose_column(self, game: ConnectFour) -> int:
        """ Return a chosen column of grid given the current game.
        """
        raise NotImplementedError

# class UserPlayer(Player):
#     """ An abstract class representing a user player of Connect 4.
#     """
#     def choose_column(self, game: ConnectFour) -> int:


class AIPlayer(Player):
    """ An abstract class representing an AI player of Connect 4.

    """
    def choose_column(self, game: ConnectFour) -> int:
        """ Return the column that is corresponding to the AI's move.
        """
        if game.player_one_moves == [] or self._game_tree is None:
            pass
        else:
            curr_move = game.get_sequence_moves()[-1]
            for subtree in self._game_tree.get_subtrees():
                if subtree.move == curr_move:
                    self._game_tree = subtree
                    break
                else:
                    self._game_tree = None

        if self._game_tree is None or self._game_tree.get_subtrees() == []:
            possible_columns = game.get_possible_column()
            return random.choice(list(possible_columns))
        else:
            possible_answer_trees = self._game_tree.get_subtrees()

            possible_scores = [tree.score for tree in possible_answer_trees]
            max_score = max(possible_scores)
            max_score_trees = [t for t in possible_answer_trees if t.score == max_score]
            random_choice_max_score_tree = random.choice(max_score_trees)
            self._game_tree = random_choice_max_score_tree
            return random_choice_max_score_tree.move[1]

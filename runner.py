"""CSC111 Winter 2023 Project: Connect 4 (Runner)

Module Description
==================

This module contains a main class GameRunner which represents the manipulation of the game
that runs in the pygame interface, with two functions run_game_interactive() and
run_game_between_ai() that represent two different types of runners.
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
"""
from typing import Optional
import pygame
from connect_four import ConnectFour
from player import Player, RandomPlayer, GreedyPlayer, ScoringPlayer
from interface import Button, GameBoard, Disc, Label
from constant import GAME_NOT_STARTED, GAMING, GAME_OVER, UNOCCUPIED, PLAYER_ONE, PLAYER_TWO, HINT, \
    SQUARESIZE, GRID_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, \
    FONT_WORDS, FONT_WIN_STATUS, BLACK, LIGHT_BLUE, WHITE


class GameRunner:
    """
    A class that assembles the instructions of a game and leads the gaming process, letting two players
    make moves alternatively.

    It has a lot of instance attributes, but we believe that they are all necessary for running such
    a large game. We tried to make the names readable and easy to understand. We also maded sure that
    the methods are neat and understandable.

    Instance attributes:
        - gane_status: an integer representing the state of the game, which is one of GAME_NOT_STARTED,
        GAMING, and GAME_OVER.
        - game: a ConnecFour instance representing the current game.
        - ai_player: Either None or a GreedyPlayer that represents the AI our user is competing against.
        - ai_search_depth: an integer representing the depth of the GameTree the AI player uses to make decisions.
        - user_goes_first: a boolean value indicating if the user goes first.

    Private instance attributes:
        - _winner: an integer representing the winner of this game, or None if there is no winner.
        - _me_first_button: a Button instance representing the interactive button which the user clicks to go first.
        - _ai_first_button: a Button instance representing the interactive button which the user clicks to go second.
        - _hint_button: a Button instance representing the interactive button which the user clicks to receive a hint.
        - _restart_button: a Button instance representing the interactive button which the user clicks to retart a game.
        - _game_board: a GameBoard instance representing the blue board on our interactive interface in which
        the discs are dropped into.
        - _hover_disc: a Disc instance representing the moving disc on top of the blue board on our interactive
        interface which indicates the current hirozontal position of the disc if it is dropped at that moment.
        - _legend: a list of Disc or Label representing the legend illustrated at the bottom of our
        interactive interface, indicating the Disc color for each player.
        - _notice_lable: a Label instance representing the instructions that appears on top of our
        interactive interface.
        - _win_label: a Label instance representing the winning message that is displayed once the game ends.

    """
    game_status: int
    game: ConnectFour
    ai_player: Optional[GreedyPlayer]
    ai_search_depth: int
    user_goes_first: Optional[bool]
    _winner: Optional[int]
    _me_first_button: Button
    _ai_first_button: Button
    _hint_button: Button
    _restart_button: Button
    _game_board: GameBoard
    _hover_disc: Disc
    _legend: list[Disc | Label]
    _notice_label: Label
    _win_label: Label

    def __init__(self, ai_search_depth: int) -> None:
        """
        Initializes the GameRunner.
        """
        self.game_status = GAME_NOT_STARTED
        self.game = ConnectFour()
        self.ai_player = None
        self.ai_search_depth = ai_search_depth
        self.user_goes_first = None
        self._winner = None

        self._me_first_button = Button(x=10 * SQUARESIZE, y=2 * SQUARESIZE, word='I go first')
        self._ai_first_button = Button(x=10 * SQUARESIZE, y=4 * SQUARESIZE, word='AI go first')
        self._hint_button = Button(x=10 * SQUARESIZE, y=6 * SQUARESIZE, word='HINT')
        self._restart_button = Button(x=10 * SQUARESIZE, y=8 * SQUARESIZE, word='RESTART')
        self._game_board = GameBoard(SQUARESIZE, 2 * SQUARESIZE)
        self._update_disabled()

        self._hover_disc = Disc(SQUARESIZE, int(1.5 * SQUARESIZE), UNOCCUPIED)

        player_one_disc = Disc(int(SQUARESIZE * 2.5), (2 + GRID_WIDTH) * SQUARESIZE, PLAYER_ONE)
        player_two_disc = Disc(int(SQUARESIZE * 6.5), (2 + GRID_WIDTH) * SQUARESIZE, PLAYER_TWO)
        player_one_label = Label((int(SQUARESIZE * 2.5), int((2.5 + GRID_WIDTH) * SQUARESIZE)), 'Player One',
                                 (FONT_WORDS, BLACK))
        player_two_label = Label((int(SQUARESIZE * 6.5), int((2.5 + GRID_WIDTH) * SQUARESIZE)), 'Player Two',
                                 (FONT_WORDS, BLACK))
        self._legend = [player_one_disc, player_two_disc, player_one_label, player_two_label]

        self._notice_label = Label((SQUARESIZE, SQUARESIZE), 'Choose if you want to go first or last!',
                                   (FONT_WORDS, BLACK))
        self._win_label = Label((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - int(0.5 * SQUARESIZE)), '',
                                (FONT_WIN_STATUS, BLACK),
                                background=(pygame.Rect(0, WINDOW_HEIGHT // 2 - SQUARESIZE, WINDOW_WIDTH, SQUARESIZE),
                                            LIGHT_BLUE))
        self._notice_label.align = 'left'
        self._win_label.visible = False

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws surface, which is the current pygame surface display of the game.
        """
        surface.fill(WHITE)
        for button in [self._me_first_button, self._ai_first_button, self._hint_button, self._restart_button]:
            button.draw(surface)
        for legend in self._legend:
            legend.draw(surface)
        self._hover_disc.draw(surface)
        self._game_board.draw(surface)
        self._notice_label.draw(surface)
        self._win_label.draw(surface)
        pygame.display.update()

    def handle_event(self, pygame_event: pygame.event, surface: pygame.Surface) -> None:
        """
        Handles the pygame_event on the surface given accordingly.
        """
        if pygame_event.type == pygame.MOUSEBUTTONUP:
            self._handle_mouse_button_up(pygame_event.pos, surface)
        elif pygame_event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(pygame_event.pos)

    def _handle_mouse_button_up(self, position: tuple[int, int], surface: pygame.Surface) -> None:
        """
        Handles the type of event which user clicks a position on the surface to advance the game.
        """
        # Press button to chooe who goes first
        if self._me_first_button.is_valid_click(position):
            self._start_gaming('User')

        elif self._ai_first_button.is_valid_click(position):
            self._start_gaming('AI')
            # AI makes the first move
            self.draw(surface)
            self._ai_makes_move()

        # Press hint button
        elif self._hint_button.is_valid_click(position):
            self._hint()

        # Press restart button
        elif self._restart_button.is_valid_click(position):
            self._restart()

        # Clicks on the game board
        elif self._game_board.is_valid_click(position):

            # User makes move
            if not self._user_makes_move(position):
                # The move is not valid (i.e., the chosen column is full).
                return

            # Draw user's move first, because AI takes some time to make move
            self.draw(surface)
            if not self._game_over():
                # AI makes move if player doesn't win
                self._ai_makes_move()

            # Handle game over case
            if self._game_over():
                self._show_winner()

    def _handle_mouse_motion(self, position: tuple[int, int]) -> None:
        """
        Handles the type of event which user moves the mouse to position on the surface
        to advance the game or change the display.
        """
        if self.game_status != GAMING:
            return

        x = position[0]
        if SQUARESIZE <= x <= 8 * SQUARESIZE:
            if self.user_goes_first:
                self._hover_disc.update_color_and_type(PLAYER_ONE)
            else:
                self._hover_disc.update_color_and_type(PLAYER_TWO)
            self._hover_disc.x = x

    def _start_gaming(self, first_player: str) -> None:
        """
        Uses first_player to update user_goes_first to the appropriate boolean value.
        Updates game_status to GAMING.

        Preconditions:
            - 0 <= move_column < 7
            - first_player == 'User' or first_player == 'AI'
        """
        if first_player == 'User':
            self.ai_player = GreedyPlayer(PLAYER_TWO, self.ai_search_depth, None)
            self.user_goes_first = True
        elif first_player == 'AI':
            self.ai_player = GreedyPlayer(PLAYER_ONE, self.ai_search_depth, None)
            self.user_goes_first = False

        self.game_status = GAMING
        self._update_disabled()
        self._notice_label.update_text('')

    def _hint(self) -> None:
        """
        Update the game grid with a hint location where the user can choose to drop the piece, so the display can be
        updated consequently.
        """
        hint_column = self.ai_player.hint_opponent(self.game)
        hint_position = self.game.get_move_position_by_column(hint_column)
        self._game_board.record_move(hint_position, HINT)

    def _restart(self) -> None:
        """ Reset the game to the condition same as when it started."""
        self.game = ConnectFour()
        self.ai_player = None
        self.user_goes_first = None
        self._winner = None
        self.game_status = GAME_NOT_STARTED
        self._update_disabled()
        self._notice_label.update_text('Choose if you want to go first or last!')
        self._win_label.visible = False
        self._game_board = GameBoard(SQUARESIZE, 2 * SQUARESIZE)
        self._hover_disc = Disc(SQUARESIZE, int(1.5 * SQUARESIZE), UNOCCUPIED)

    def _ai_makes_move(self) -> None:
        """Let the AI player make a move and record it."""
        ai_move_column = self.ai_player.choose_column(self.game)
        self._record_move(ai_move_column, 'AI')

    def _user_makes_move(self, mouse_position: tuple[int, int]) -> bool:
        """
        Make and record user's move according to mouse_position and return True if it is a valid position.
        Display 'Choose another column!' and return False if it is not valid.
        """
        self._game_board.remove_hint()
        user_move_column = self._game_board.get_move_column(mouse_position)
        if user_move_column not in self.game.get_possible_columns():
            # User didn't select a valid move column
            self._notice_label.update_text('Choose another column!')
            return False

        self._notice_label.update_text('')
        self._record_move(user_move_column, 'User')
        self._hover_disc.update_color_and_type(UNOCCUPIED)
        return True

    def _record_move(self, move_column: int, player_type: str) -> None:
        """
        Record a move for the given player_type at the appropriate position given move_column.

        Preconditions:
            - 0 <= move_column < 7
            - player_type == 'User' or player_type == 'AI'
        """
        if (player_type == 'User' and self.user_goes_first) or (player_type == 'AI' and not self.user_goes_first):
            disc_type = PLAYER_ONE
        else:
            disc_type = PLAYER_TWO
        move_position = self.game.get_move_position_by_column(move_column)
        self._game_board.record_move(move_position, disc_type)
        self.game.record_player_move(move_column)

    def _game_over(self) -> bool:
        """
        Return a boolean value representing whether the game is over.
        """
        self._winner = self.game.get_winner()
        if self._winner is None:
            return False
        return True

    def _show_winner(self) -> None:
        """ Display a lable showing the result of the game.

        Update the game_status to GAME_OVER status.
        """
        self.game_status = GAME_OVER
        if self._winner == UNOCCUPIED:
            self._win_label.update_text('TIE!')
        elif self._winner == self.ai_player.player_num:
            self._win_label.update_text('AI Wins!')
        else:
            self._win_label.update_text('You Win!')
        self._win_label.visible = True
        self._update_disabled()
        self._notice_label.update_text('Press Restart for a new game!')
        self._hover_disc.update_color_and_type(UNOCCUPIED)

    def _update_disabled(self) -> None:
        """
        Update the four buttons‘ disabled attribute and gameboard's disabled attribute according to self.game_status.
        """
        if self.game_status == GAME_NOT_STARTED:
            self._me_first_button.disabled = False
            self._ai_first_button.disabled = False
            self._hint_button.disabled = True
            self._restart_button.disabled = False
            self._game_board.disabled = True
        elif self.game_status == GAMING:
            self._me_first_button.disabled = True
            self._ai_first_button.disabled = True
            self._hint_button.disabled = False
            self._restart_button.disabled = False
            self._game_board.disabled = False
        elif self.game_status == GAME_OVER:
            self._me_first_button.disabled = True
            self._ai_first_button.disabled = True
            self._hint_button.disabled = True
            self._restart_button.disabled = False
            self._game_board.disabled = True


def run_game_interactive() -> None:
    """
    Run a game in the console between the user and AI, allowing the user to choose if they want to go first.
    """
    connect_four = ConnectFour()

    first_player = input('Who goes first? Please type AI or Human:')
    while first_player not in {'AI', 'Human'}:
        first_player = input('Invalid input. Please type AI or Human.')

    if first_player == 'AI':
        ai_player = _get_player_from_console(PLAYER_ONE)
        second_player = 'Human'
    else:
        ai_player = _get_player_from_console(PLAYER_ONE)
        second_player = 'AI'

    current_player = first_player

    while connect_four.get_winner() is None:
        if current_player == 'Human':
            player_move = int(input('Please choose column:'))
            while player_move < 0 or player_move > 6:
                player_move = int(input('Invalid input. Please enter a number between 0 and 6.'))
            connect_four.record_player_move(player_move)
            current_player = 'AI'
        else:
            print('AI is thinking...')
            connect_four.record_player_move(ai_player.choose_column(connect_four))
            current_player = 'Human'
        print(connect_four)

    if connect_four.get_winner() == PLAYER_ONE:
        print(f'{first_player} Wins!')
    elif connect_four.get_winner() == PLAYER_TWO:
        print(f'{second_player} Wins!')
    else:
        print('Ties!')


def run_game_between_ai() -> None:
    """
    Run a game between two AIs in console, allowing the user to input the number of games they want the AI to play.
    The results of each game and the accumulative result will be printed.
    """
    game_number = int(input('How many games do you want to run?'))
    while game_number <= 0:
        game_number = int(input('Invalid input. Please enter a number greater than 0.'))

    stats_so_far = [0, 0, 0]

    print('Choose the first AI player.')
    first_ai = _get_player_from_console(PLAYER_ONE)
    second_ai = _get_player_from_console(PLAYER_TWO)

    for i in range(game_number):
        connect_four = ConnectFour()
        first_player = first_ai.copy()
        second_player = second_ai.copy()
        current_player = first_player

        while connect_four.get_winner() is None:

            move_column = current_player.choose_column(connect_four)
            connect_four.record_player_move(move_column)

            if current_player == first_player:
                current_player = second_player
            else:
                current_player = first_player

        winner = connect_four.get_winner()
        if winner == PLAYER_ONE:
            stats_so_far[0] += 1
            print(f'{i + 1}th game, Player one wins.')
        elif winner == PLAYER_TWO:
            stats_so_far[1] += 1
            print(f'{i + 1}th game, Player two wins.')
        else:
            stats_so_far[2] += 1
            print(f'{i + 1}th game, tie.')
        print(connect_four)

        print(f'Player one wins {stats_so_far[0]} times. Player two wins {stats_so_far[1]} times. Game ties '
              f'{stats_so_far[2]} times.')


def _get_player_from_console(player_number: int) -> Player:
    """
    Returns the type of AI Player that user chooses in console. A user input of 1 indicates Random Player, 2 indicates
    Scoring Player, 3 indicates Greedy Player. Whether this AI player goes first will be dependent on player_number.
    Player_number == PLAYER_ONE indicates AI goes first, Player_number == PLAYER_TWO indicates AI goes second.
    """
    print('Please choose an AI Player. Enter a number from 1 to 3.')
    player_type = int(input('1 = Random Player, 2 = Scoring Player, 3 = Greedy Player'))
    while player_type < 1 or player_type > 3:
        player_type = int(input('Invalid input. Please enter a number from 1 to 3.'))

    if player_type == 1:
        return RandomPlayer(player_number)
    elif player_type == 2:
        return ScoringPlayer(player_number)
    else:
        print('Please enter a positive integer as the search depth of the Greedy Player.')
        search_depth = int(input('If the number is too large (>= 6), it may take a long time to compute a result.'))
        while search_depth <= 1:
            search_depth = int(input('Invalid input. Please enter an integer greater than 1.'))
        return GreedyPlayer(player_number, search_depth, None)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'max-nested-blocks': 4,
        'extra-imports': ['typing', 'pygame', 'connect_four', 'player', 'interface', 'constant'],
        'disable': ['no-member', 'too-many-instance-attributes'],
        'allowed-io': ['run_game_interactive', 'run_game_between_ai', '_get_player_from_console']
    })

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
    ...
    It has a lot of instance attributes, but we believe that they are all necessary for running such
    a large game. We tried to make the names readable and easy to understand. We also maded sure that
    the methods are neat and understandable.
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
        # TODO
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
        # TODO
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
        # TODO
        """
        if pygame_event.type == pygame.MOUSEBUTTONUP:
            self._handle_mouse_button_up(pygame_event.pos, surface)
        elif pygame_event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(pygame_event.pos)

    def _handle_mouse_button_up(self, position: tuple[int, int], surface: pygame.Surface) -> None:
        """
        ...
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
        # TODO
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
        ...
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
        ...
        """
        hint_column = self.ai_player.hint_opponent(self.game)
        hint_position = self.game.get_move_position_by_column(hint_column)
        self._game_board.record_move(hint_position, HINT)

    def _restart(self) -> None:
        """
        ...
        """
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
        """
        ...
        """
        ai_move_column = self.ai_player.choose_column(self.game)
        self._record_move(ai_move_column, 'AI')

    def _user_makes_move(self, mouse_position: tuple[int, int]) -> bool:
        """
        ...
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
        ...
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
        ...
        """
        self._winner = self.game.get_winner()
        if self._winner is None:
            return False
        return True

    def _show_winner(self) -> None:
        """
        ...
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
        update the four buttons disabled attribute and gameboard's disabled attribute according to self.game_status
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
    ...
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
    ...
    """
    game_number = int(input('How many games do you want to run?'))
    while game_number <= 0:
        game_number = int(input('Invalid input. Please enter a number greater than 0.'))
    stats_so_far = [0, 0, 0]

    print('Choose the first AI player.')
    ai_first = _get_player_from_console(PLAYER_ONE)
    ai_second = _get_player_from_console(PLAYER_TWO)

    for i in range(game_number):
        connect_four = ConnectFour()
        first_player = _copy_player(ai_first)
        second_player = _copy_player(ai_second)
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
    ...
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
        while search_depth <= 0:
            search_depth = int(input('Invalid input. Please enter an integer greater than 0.'))
        return GreedyPlayer(player_number, search_depth, None)


def _copy_player(player: Player) -> Player:
    """
    ...
    """
    if isinstance(player, RandomPlayer):
        return RandomPlayer(player.player_num)
    elif isinstance(player, ScoringPlayer):
        return ScoringPlayer(player.player_num)
    elif isinstance(player, GreedyPlayer):
        return GreedyPlayer(player.player_num, player.depth, None)


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

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
import pygame
from connect_four import ConnectFour
from player import RandomPlayer, GreedyPlayer, ScoringPlayer
from interface import Button, GameBoard, Disc, Label
from constant import GAME_NOT_STARTED, GAMING, GAME_OVER, UNOCCUPIED, PLAYER_ONE, PLAYER_TWO, HINT, \
    SQUARESIZE, GRID_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, \
    FONT_WORDS, FONT_WIN_STATUS, BLACK, LIGHT_BLUE, WHITE


class GameRunner:
    """
    ...
    """
    def __init__(self, ai_search_depth: int) -> None:
        """
        # TODO
        """
        self.game_status = GAME_NOT_STARTED

        self.game = ConnectFour()
        self._AI_player = None
        self.AI_search_depth = ai_search_depth
        self.user_goes_first = None
        self._winner = None

        self._me_first_button = Button(x=10 * SQUARESIZE, y=2 * SQUARESIZE, word='I go first')
        self._ai_first_button = Button(x=10 * SQUARESIZE, y=4 * SQUARESIZE, word='AI go first')
        self._hint_button = Button(x=10 * SQUARESIZE, y=6 * SQUARESIZE, word='HINT')
        self._restart_button = Button(x=10 * SQUARESIZE, y=8 * SQUARESIZE, word='RESTART')
        self._buttons = [self._me_first_button, self._ai_first_button, self._hint_button, self._restart_button]
        self._game_board = GameBoard(SQUARESIZE, 2 * SQUARESIZE)
        self._update_disabled()

        self._hover_disc = Disc(SQUARESIZE, int(1.5 * SQUARESIZE), UNOCCUPIED)

        player_one_disc = Disc(int(SQUARESIZE * 2.5), (2 + GRID_WIDTH) * SQUARESIZE, PLAYER_ONE)
        player_two_disc = Disc(int(SQUARESIZE * 6.5), (2 + GRID_WIDTH) * SQUARESIZE, PLAYER_TWO)
        player_one_label = Label(int(SQUARESIZE * 2.5), int((2.5 + GRID_WIDTH) * SQUARESIZE), 'Player One',
                                 FONT_WORDS, BLACK)
        player_two_label = Label(int(SQUARESIZE * 6.5), int((2.5 + GRID_WIDTH) * SQUARESIZE), 'Player Two',
                                 FONT_WORDS, BLACK)
        self._legend = [player_one_disc, player_two_disc, player_one_label, player_two_label]

        self._notice_label = Label(SQUARESIZE, SQUARESIZE, 'Choose if you want to go first or last!',
                                   FONT_WORDS, BLACK, align='left')
        self._win_label = Label(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - int(0.5 * SQUARESIZE), '', FONT_WIN_STATUS,
                                BLACK, visible=False, background_rect=pygame.Rect(0, WINDOW_HEIGHT // 2 - SQUARESIZE,
                                                                                  WINDOW_WIDTH, SQUARESIZE),
                                background_color=LIGHT_BLUE)

    def draw(self, surface: pygame.Surface) -> None:
        """
        # TODO
        """
        surface.fill(WHITE)
        for button in self._buttons:
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
            self.AI_player = GreedyPlayer(PLAYER_TWO, self.AI_search_depth, None)
            self.user_goes_first = True
        elif first_player == 'AI':
            self.AI_player = GreedyPlayer(PLAYER_ONE, self.AI_search_depth, None)
            self.user_goes_first = False

        self.game_status = GAMING
        self._update_disabled()
        self._notice_label.update_text('')

    def _hint(self) -> None:
        """
        ...
        """
        hint_column = self.AI_player.hint_opponent(self.game)
        hint_position = self.game.get_move_position_by_column(hint_column)
        self._game_board.record_move(hint_position, HINT)

    def _restart(self) -> None:
        """
        ...
        """
        self.game = ConnectFour()
        self.AI_player = None
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
        ai_move_column = self.AI_player.choose_column(self.game)
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
        elif self._winner == self.AI_player.player_num:
            self._win_label.update_text('AI Wins!')
        else:
            self._win_label.update_text('You Win!')
        self._win_label.visible = True
        self._update_disabled()
        self._notice_label.update_text('Press Restart for a new game!')
        self._hover_disc.update_color_and_type(UNOCCUPIED)

    def _update_disabled(self) -> None:
        """
        # TODO
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
    ...


def run_game_between_ai() -> None:
    """
    ...
    """
    ...


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

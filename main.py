"""CSC111 Winter 2023 Project: Connect 4 (Main)
Module Description
==================
This module contains the codes and functions that are necessary to run the entire program from start to finish.
By reading the *docstring* of this file, you can gain insights into the
role and functionality of these codes and functions as well as how they contribute to this project as a whole.
Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of the
Teaching Stream of CSC111 at the University of Toronto St. George campus.
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.
This file is Copyright (c) 2023 Yige (Amanda) Wu, Sunyi (Alysa) Liu, Lecheng (Joyce) Qu, and Xi (Olivia) Yan.
"""
from __future__ import annotations

import sys
import math
import pygame
from typing import Optional

from player import RandomPlayer, GreedyPlayer, ScoringPlayer

from interface import Button, GameBoard, Disc, Label, \
    RED, DARK_RED, YELLOW, DARK_YELLOW, BLUE, LIGHT_BLUE, DARK_BLUE, GREY, DARK_GREY, BLACK, WHITE, \
    GRID_WIDTH, GRID_HEIGHT, SQUARESIZE, \
    UNOCCUPIED, PLAYER_ONE, PLAYER_TWO, HINT, \
    WINDOW_WIDTH, WINDOW_HEIGHT, \
    SIZE, FONT_WORDS, FONT_WIN_STATUS

from connect_four import ConnectFour

GAME_NOT_STARTED, GAMING, GAME_OVER = -1, 0, 1


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

        self._me_first_button = Button(x=10 * SQUARESIZE, y=2 * SQUARESIZE, word='I go first')
        self._ai_first_button = Button(x=10 * SQUARESIZE, y=4 * SQUARESIZE, word='AI go first')
        self._hint_button = Button(x=10 * SQUARESIZE, y=6 * SQUARESIZE, word='HINT')
        self._restart_button = Button(x=10 * SQUARESIZE, y=8 * SQUARESIZE, word='RESTART')
        self._buttons = [self._me_first_button, self._ai_first_button, self._hint_button, self._restart_button]
        self._update_buttons_disabled()

        self._game_board = GameBoard(SQUARESIZE, 2 * SQUARESIZE)
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
        if self.game_status == GAME_NOT_STARTED:
            if not (self._me_first_button.is_valid_click(position)) and \
                    not (self._ai_first_button.is_valid_click(position)):
                return

            if self._me_first_button.is_valid_click(position):
                self.AI_player = GreedyPlayer(PLAYER_TWO, self.AI_search_depth, None)
                self.user_goes_first = True
            else:
                self.AI_player = GreedyPlayer(PLAYER_ONE, self.AI_search_depth, None)
                self.user_goes_first = False

            self.game_status = GAMING
            self._update_buttons_disabled()
            self._notice_label.update_text('')

            # AI makes the first move
            if not self.user_goes_first:
                move_column = self.AI_player.choose_column(self.game)
                move_position = self.game.get_move_position_by_column(move_column)
                self._game_board.record_move(move_position, PLAYER_ONE)
                self.game.record_player_move(move_column)

        elif self.game_status == GAMING:
            # Press hint button
            if self._hint_button.is_valid_click(position):
                hint_column = self.AI_player.hint_opponent(self.game)
                hint_position = self.game.get_move_position_by_column(hint_column)
                self._game_board.record_move(hint_position, HINT)
                return

            elif self._restart_button.is_valid_click(position):
                self._restart()
                return

            # User make move
            elif self._game_board.is_valid_click(position) is not None:
                self._game_board.remove_hint()
                user_move_column = self._game_board.get_move_column(position)
                if user_move_column not in self.game.get_possible_columns():
                    self._notice_label.update_text('Choose another column!')
                    return

                self._notice_label.update_text('')
                move_position = self.game.get_move_position_by_column(user_move_column)
                if self.user_goes_first:
                    disc_type = PLAYER_ONE
                else:
                    disc_type = PLAYER_TWO
                self._game_board.record_move(move_position, disc_type)
                self.game.record_player_move(user_move_column)

                self._hover_disc.update_color_and_type(UNOCCUPIED)
                self.draw(surface)

            winner = self.game.get_winner()
            if winner is None:
                # AI makes move
                ai_move_column = self.AI_player.choose_column(self.game)
                move_position = self.game.get_move_position_by_column(ai_move_column)
                if self.user_goes_first:
                    disc_type = PLAYER_TWO
                else:
                    disc_type = PLAYER_ONE
                self._game_board.record_move(move_position, disc_type)
                self.game.record_player_move(ai_move_column)

            winner = self.game.get_winner()
            if winner is None:
                return

            # Winner exists. Game over.
            self.game_status = GAME_OVER
            if winner == UNOCCUPIED:
                self._win_label.update_text('TIE!')
            elif winner == self.AI_player.player_num:
                self._win_label.update_text('AI Wins!')
            else:
                self._win_label.update_text('You Win!')
            self._win_label.visible = True
            self._update_buttons_disabled()
            self._notice_label.update_text('Press Restart for a new game!')
            self._hover_disc.update_color_and_type(UNOCCUPIED)

        elif self.game_status == GAME_OVER:
            if self._restart_button.is_valid_click(position):
                self._restart()

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

    def _restart(self) -> None:
        """
        ...
        """
        self.game = ConnectFour()
        self.AI_player = None
        self.user_goes_first = None
        self.game_status = GAME_NOT_STARTED
        self._update_buttons_disabled()
        self._notice_label.update_text('Choose if you want to go first or last!')
        self._win_label.visible = False
        self._game_board = GameBoard(SQUARESIZE, 2 * SQUARESIZE)
        self._hover_disc = Disc(SQUARESIZE, int(1.5 * SQUARESIZE), UNOCCUPIED)

    def _update_buttons_disabled(self) -> None:
        """
        # TODO
        """
        if self.game_status == GAME_NOT_STARTED:
            self._me_first_button.disabled = False
            self._ai_first_button.disabled = False
            self._hint_button.disabled = True
            self._restart_button.disabled = False
        elif self.game_status == GAMING:
            self._me_first_button.disabled = True
            self._ai_first_button.disabled = True
            self._hint_button.disabled = False
            self._restart_button.disabled = False
        elif self.game_status == GAME_OVER:
            self._me_first_button.disabled = True
            self._ai_first_button.disabled = True
            self._hint_button.disabled = True
            self._restart_button.disabled = False


if __name__ == '__main__':

    pygame.init()  # pygame needs to be initialized before defining FONT
    screen = pygame.display.set_mode(SIZE)
    pygame.display.flip()
    pygame.display.set_caption("CONNECT FOUR")
    clock = pygame.time.Clock()

    game_runner = GameRunner(5)

    # draw_window(screen, ConnectFour(), game_runner.buttons)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            game_runner.handle_event(event, screen)

        game_runner.draw(screen)
        pygame.display.update()
        clock.tick(50)

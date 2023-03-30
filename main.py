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
from player import RandomPlayer
from interface import draw_window, Button, drop_piece, is_valid_location, get_next_open_row
# FIXME: 如果加了imprt的话会显示circular import error

import sys
import math
import pygame

from connect_four import ConnectFour

pygame.init()  # pygame needs to be initialized before defining FONT

UNOCCUPIED, PLAYER_ONE, PLAYER_TWO = -1, 0, 1
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 75
RADIUS = int(SQUARESIZE / 3)
WINDOW_WIDTH, WINDOW_HEIGHT = SQUARESIZE * 11, SQUARESIZE * 11
SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

BUTTOM_COLUMN_WIDTH = ...
FONT = pygame.font.Font(None, 75)
COLOR_PLAYER_ONE, COLOR_PLAYER_TWO = (255, 71, 71), (255, 196, 0)
BLUE, WHITE, BLACK = (65, 108, 234), (255, 255, 255), (0,0,0)

connect_four_game = ConnectFour()
game_over = False

screen = pygame.display.set_mode(SIZE)

draw_window(screen, connect_four_game)
pygame.display.update()

user_go_first = None
go_first_button = BUTTON()
go_second_button = BUTTON()

while not go_first_button.clicked and not go_second_button.clicked:
    for event in pygame.event.get():
        label_choose_order = FONT.render("Choose if you want to go first or last!", True, WHITE)
        screen.blit(label_choose_order, (SQUARESIZE + 40, SQUARESIZE + 10))

pygame.draw.rect(screen, BLACK, (SQUARESIZE, SQUARESIZE, 7*SQUARESIZE, SQUARESIZE))


if go_first_button.clicked:
    user_go_first = True
else:
    user_go_first = False

AI_player = RandomPlayer(not user_go_first)


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (SQUARESIZE, SQUARESIZE, 7*SQUARESIZE, SQUARESIZE))
            posx, posy = event.pos[0], event.pos[1]
            if posx in [SQUARESIZE, 8*SQUARESIZE] and posy in [SQUARESIZE, 8*SQUARESIZE]: #posx, posy in the region for selection and player is user :
                pygame.draw.circle(screen, BLACK, (posx, int(SQUARESIZE/2 + SQUARESIZE)), RADIUS) #Olivia 改一下颜色
            else:
                pass

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            posx, posy = event.pos[0], event.pos[1]
            if posx in [SQUARESIZE, 8 * SQUARESIZE] and posy in [SQUARESIZE, 8 * SQUARESIZE]:
                # making a selection on game board
                # ask player 1 input
                col = None
                if connect_four_game.get_current_player() == 0:
                    if user_go_first:
                        col = int(math.floor(posx/SQUARESIZE) - 1)

                        # col = int(input("Player 1 Make your selection: (0, 6)"))
                        if is_valid_location(connect_four_game.grid, col):
                            row = get_next_open_row(connect_four_game.grid, col)
                            drop_piece(connect_four_game.grid, row, col, 0)
                    else:
                        col = AI_player.choose_column(connect_four_game)
                        row = get_next_open_row(connect_four_game.grid, col)
                        drop_piece(connect_four_game.grid, row, col, 1)

                # ask player 2 input
                else:  # player 2 turn
                    if user_go_first:
                        col = AI_player.choose_column(connect_four_game)
                        row = get_next_open_row(connect_four_game.grid, col)
                        drop_piece(connect_four_game.grid, row, col, 0)
                    else:
                        col = int(math.floor(posx/SQUARESIZE) - 1)

                        if is_valid_location(connect_four_game.grid, col):
                            row = get_next_open_row(connect_four_game.grid, col)
                            drop_piece(connect_four_game.grid, row, col, 1)

                connect_four_game.record_player_move(col)

                if connect_four_game.get_winner() is not None:
                    game_over = True

            # redraw after a click is made
            draw_window(screen, connect_four_game)


if (connect_four_game.get_winner() == PLAYER_ONE and user_go_first) or\
        (connect_four_game.get_winner() == PLAYER_TWO and not user_go_first):
    label = FONT.render("You win!", True, BLACK)
else:
    label = FONT.render("AI wins!", True, BLACK)
screen.blit(label, (SQUARESIZE + 40, 10))


# def drop_piece(board, row, col, piece):
#     board[row][col] = piece
#
# def is_valid_location(board, col):
#     # check if the location is valid
#     return board[ROW_COUNT - 1][col] == -1
#
# def get_next_open_row(board, col):
#     for r in range(ROW_COUNT):
#         if board[r][col] == -1:
#             return r

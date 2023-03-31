# """CSC111 Winter 2023 Project: Connect 4 (Main)
#
# Module Description
# ==================
#
# This module contains the codes and functions that are necessary to run the entire program from start to finish.
# By reading the *docstring* of this file, you can gain insights into the
# role and functionality of these codes and functions as well as how they contribute to this project as a whole.
#
# Copyright and Usage Information
# ===============================
#
# This file is provided solely for the personal and private use of the
# Teaching Stream of CSC111 at the University of Toronto St. George campus.
# All forms of distribution of this code, whether as given or with any changes, are
# expressly prohibited.
#
# This file is Copyright (c) 2023 Yige (Amanda) Wu, Sunyi (Alysa) Liu, Lecheng (Joyce) Qu, and Xi (Olivia) Yan.
# """
# from __future__ import annotations
# from player import RandomPlayer
#
# import time
# import sys
# import math
# import pygame
# from interface import draw_window, Button, drop_piece, is_valid_location
#
# from connect_four import ConnectFour
#
# pygame.init()  # pygame needs to be initialized before defining FONT
#
# # UNOCCUPIED, PLAYER_ONE, PLAYER_TWO = -1, 0, 1
# # ROW_COUNT = 6
# # COLUMN_COUNT = 7
# # SQUARESIZE = 75
# # RADIUS = int(SQUARESIZE / 3)
# # WINDOW_WIDTH, WINDOW_HEIGHT = SQUARESIZE * 11, SQUARESIZE * 11
# # SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
# #
# # BUTTOM_COLUMN_WIDTH = ...
# # FONT = pygame.font.Font(None, 75)
# # COLOR_PLAYER_ONE, COLOR_PLAYER_TWO = (255, 71, 71), (255, 196, 0)
# # BLUE, WHITE, BLACK = (65, 108, 234), (255, 255, 255), (0,0,0)
#
# from interface import SQUARESIZE, RADIUS, WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_PLAYER_ONE, COLOR_PLAYER_TWO, BLUE, WHITE, \
#     BLACK, ROW_COUNT, COLUMN_COUNT, FONT, PLAYER_ONE, PLAYER_TWO, SIZE
#
#
# connect_four_game = ConnectFour()
# game_over = False
#
# screen = pygame.display.set_mode(SIZE)
# pygame.display.flip()
# draw_window(screen, connect_four_game)
# pygame.display.update()
#
# user_go_first = None
# go_first_button = Button(x=10*SQUARESIZE, y=2*SQUARESIZE, word='I go first')
# go_first_button.draw(screen)
# go_second_button = Button(x=10*SQUARESIZE, y=5*SQUARESIZE, word='AI go first')
# go_second_button.draw(screen)
#
# print(go_first_button.clicked)
#
# label_choose_order = FONT.render("Choose if you want to go first or last!", True, BLACK)
# screen.blit(label_choose_order, (SQUARESIZE + 40, SQUARESIZE + 10))
# print(go_first_button.clicked)
#
# while not go_first_button.clicked and not go_second_button.clicked:
#     print(go_first_button.clicked)
#     for event in pygame.event.get():
#         if event.type == pygame.MOUSEBUTTONUP:
#             position = event.pos
#             go_first_button.is_valid(position)
#             go_second_button.is_valid(position)
# print(go_first_button.clicked)
#
# pygame.draw.rect(screen, WHITE, (SQUARESIZE, SQUARESIZE, 7*SQUARESIZE, SQUARESIZE))
#
#
# <<<<<<< Updated upstream
# if go_first_button.clicked:
#     user_go_first = True
# else:
#     user_go_first = False
# =======
# while True:
#     print(game_status)
#
#     if game_status == 'before_game':
#         print('restarted')
#         connect_four_game = ConnectFour()
#         go_first_button.reset_click(False)
#         go_second_button.reset_click(False)
#         restart_button.reset_click(False)
# >>>>>>> Stashed changes
#
# AI_player = RandomPlayer(not user_go_first)
#
#
# while not game_over:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             print(1)
#             sys.exit()
#
#         if event.type == pygame.MOUSEMOTION:
#             pygame.draw.rect(screen, WHITE, (SQUARESIZE, SQUARESIZE, 7*SQUARESIZE, SQUARESIZE))
#             pygame.display.update()
#             posx, posy = event.pos[0], event.pos[1]
#             if posx in [SQUARESIZE, 8*SQUARESIZE] and posy in [SQUARESIZE, 8*SQUARESIZE]: #posx, posy in the region for selection and player is user :
#                 pygame.draw.circle(screen, BLACK, (posx, int(SQUARESIZE/2 + SQUARESIZE)), RADIUS) #Olivia 改一下颜色
#                 pygame.display.update()
#             else:
#                 pass
#             # pygame.draw.rect(screen, WHITE, (SQUARESIZE, SQUARESIZE, 7 * SQUARESIZE, SQUARESIZE))
#         print(2)
#         pygame.display.update()
#         draw_window(screen, connect_four_game, [hint_button, restart_button, go_first_button, go_second_button])
#
# <<<<<<< Updated upstream
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             print(3)
#             print(connect_four_game.grid)
#             posx, posy = event.pos[0], event.pos[1]
#             if SQUARESIZE <= posx <= 8 * SQUARESIZE and SQUARESIZE <= posy <= 8 * SQUARESIZE:
#                 # making a selection on game board
#                 # ask player 1 input
#                 print(5)
#                 col = None
# =======
#         user_go_first = None
#
#         while not go_first_button.clicked and not go_second_button.clicked:
#             for event in pygame.event.get():
#                 if event.type == pygame.MOUSEBUTTONUP:
#                     position = event.pos
#                     go_first_button.is_valid(position)
#                     go_second_button.is_valid(position)
#                 elif event.type == pygame.QUIT:
#                     sys.exit()
#
#         # pygame.draw.rect(screen, WHITE, (SQUARESIZE, SQUARESIZE, 7 * SQUARESIZE, SQUARESIZE))
#         if go_first_button.clicked:
#             user_go_first = True
#         else:
#             user_go_first = False
#
#         AI_player = RandomPlayer(not user_go_first)
#
#         game_status = 'gaming'
#     elif game_status == 'gaming':
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 sys.exit()
#
#             if event.type == pygame.MOUSEMOTION:
#                 pygame.draw.rect(screen, WHITE, (0.5 * SQUARESIZE, SQUARESIZE, 8.5 * SQUARESIZE, SQUARESIZE))
#                 pygame.display.update()
#                 posx, posy = event.pos[0], event.pos[1]
#                 if SQUARESIZE <= posx <= 8 * SQUARESIZE and SQUARESIZE <= posy <= 8 * SQUARESIZE:  # posx, posy in the region for selection and player is user :
#                     pygame.draw.circle(screen, BLACK, (posx, int(SQUARESIZE / 2 + SQUARESIZE)), RADIUS)  # Olivia 改一下颜色
#                     pygame.display.update()
#                 # else:
#                 #     pass
#                 # pygame.draw.rect(screen, WHITE, (SQUARESIZE, SQUARESIZE, 7 * SQUARESIZE, SQUARESIZE))
#             pygame.display.update()
#
#             if user_go_first:
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     posx, posy = event.pos[0], event.pos[1]
#                     if SQUARESIZE <= posx <= 8 * SQUARESIZE and SQUARESIZE <= posy <= 8 * SQUARESIZE:  # if player click the board
#                         col = None
#                         if connect_four_game.get_current_player() == PLAYER_ONE:
#                             col = int(math.floor(posx / SQUARESIZE) - 1)
#
#                             valid = is_valid_location(connect_four_game, col)
#                             if valid:
#                                 drop_piece(connect_four_game, col)
#                                 draw_window(screen, connect_four_game, [hint_button, restart_button, go_first_button, go_second_button])
#                                 if connect_four_game.get_winner() is not None:
#                                     game_status = 'game_over'
#                                     break
#
#                                 time.sleep(1)
#
#                                 col_AI = AI_player.choose_column(connect_four_game)
#                                 drop_piece(connect_four_game, col_AI)
#                                 draw_window(screen, connect_four_game, [hint_button, restart_button, go_first_button, go_second_button])
#
#                                 if connect_four_game.get_winner() is not None:
#                                     game_status = 'game_over'
#                                     break
#                             else:
#                                 label_not_valid = FONT.render("Choose another column!", True, BLACK)
#                                 screen.blit(label_not_valid, (SQUARESIZE + 40, SQUARESIZE + 10))
#                     elif hint_button.is_valid(event.pos):  # player click HINT button:
#                         ...
#                     elif restart_button.is_valid(event.pos):
#                         game_status = 'before_game'
#                         break
#             else:  # AI goes first
#
# >>>>>>> Stashed changes
#                 if connect_four_game.get_current_player() == PLAYER_ONE:
#                     print(4)
#                     if user_go_first:
#                         col = int(math.floor(posx/SQUARESIZE) - 1)
#
#                         # col = int(input("Player 1 Make your selection: (0, 6)"))
#                         valid = is_valid_location(connect_four_game, col)
#                         if valid:
#                             drop_piece(connect_four_game, col)
#                             draw_window(screen, connect_four_game)
#                             if connect_four_game.get_winner() is not None:
#                                 game_over = True
#                                 draw_window(screen, connect_four_game)
#                                 break
#
#                             time.sleep(1)
#                             print(6)
#                             col_AI = AI_player.choose_column(connect_four_game)
#                             drop_piece(connect_four_game, col_AI)
#                             print(connect_four_game.get_current_player())
#                             draw_window(screen, connect_four_game)
#
# <<<<<<< Updated upstream
#                             if connect_four_game.get_winner() is not None:
#                                 game_over = True
#                                 draw_window(screen, connect_four_game)
#                                 break
#                         else:
#                             print("NOT VALID")
#                             label_not_valid = FONT.render("Choose another column!", True, BLACK)
#                             screen.blit(label_not_valid, (SQUARESIZE + 40, SQUARESIZE + 10))
#                             print(connect_four_game.get_current_player())
# =======
#                             valid = is_valid_location(connect_four_game, col)
#                             if valid:
#                                 drop_piece(connect_four_game, col)
#                                 draw_window(screen, connect_four_game, [hint_button, restart_button, go_first_button, go_second_button])
#                                 if connect_four_game.get_winner() is not None:
#                                     game_status = 'game_over'
#                                     break
#
#                                 print('567')
#
#                                 time.sleep(1)
#                                 print('haha')
#
#                             else:
#                                 print("NOT VALID")
#                                 label_not_valid = FONT.render("Choose another column!", True, BLACK)
#                                 screen.blit(label_not_valid, (SQUARESIZE + 40, SQUARESIZE + 10))
#                                 print(connect_four_game.get_current_player())
#                     elif hint_button.is_valid(event.pos):  # player click HINT button:
#                         ...
#                     elif restart_button.is_valid(event.pos):
#                         game_status = 'before_game'
#                         break
#                 print('A1')
#             print('A2')
#         print('A3')
#
#     elif game_status == 'game_over':
#         print('in')
#         if (connect_four_game.get_winner() == PLAYER_ONE and user_go_first) or \
#                 (connect_four_game.get_winner() == PLAYER_TWO and not user_go_first):
#             print('I won')
#             label = FONT.render("You win!", True, BLACK)
#             screen.blit(label, (SQUARESIZE, 10))
#
#         else:
#             print('noooo')
#             label = FONT.render("AI wins!", True, BLACK)
#             screen.blit(label, (SQUARESIZE, 10))
#
#         pygame.display.update()
#         time.sleep(1)
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONUP:
#                 if restart_button.is_valid(event.pos):
#                     game_status = 'before_game'
#                     break
#
#     else:
#         print('Invalid game_status')
# >>>>>>> Stashed changes
#
#
#
#                 # ask player 2 input
#                 else:  # player 2 turn
#                     print('Player 2 turn')
#                     if user_go_first:
#                         print(7)
#                         col_AI = AI_player.choose_column(connect_four_game)
#                         drop_piece(connect_four_game, col_AI)
#                         draw_window(screen, connect_four_game)
#
#                         if connect_four_game.get_winner() is not None:
#                             game_over = True
#                             draw_window(screen, connect_four_game)
#                             break
#
#                         print(8)
#                         col = int(math.floor(posx/SQUARESIZE) - 1)
#
#                         valid = is_valid_location(connect_four_game, col)
#                         if valid:
#                             drop_piece(connect_four_game, col)
#                             draw_window(screen, connect_four_game)
#                             time.sleep(1)
#                         else:
#                             label_not_valid = FONT.render("Choose another column!", True, BLACK)
#                             screen.blit(label_not_valid, (SQUARESIZE + 40, SQUARESIZE + 10))
#
#                         if connect_four_game.get_winner() is not None:
#                             game_over = True
#                             draw_window(screen, connect_four_game)
#                             break
#
#
#
#                 # connect_four_game.record_player_move(col)
#                 # pygame.draw.rect(screen, WHITE, (SQUARESIZE, SQUARESIZE, 7 * SQUARESIZE, SQUARESIZE))
#
#                 if connect_four_game.get_winner() is not None:
#                     game_over = True
#
#             # redraw after a click is made
#             # draw_window(screen, connect_four_game)
#
#
# if (connect_four_game.get_winner() == PLAYER_ONE and user_go_first) or\
#         (connect_four_game.get_winner() == PLAYER_TWO and not user_go_first):
#     label = FONT.render("You win!", True, BLACK)
#
# else:
#     label = FONT.render("AI wins!", True, BLACK)
# screen.blit(label, (SQUARESIZE + 40, 10))
# time.sleep(2)
#
#
# # def drop_piece(board, row, col, piece):
# #     board[row][col] = piece
# #
# # def is_valid_location(board, col):
# #     # check if the location is valid
# #     return board[ROW_COUNT - 1][col] == -1
# #
# # def get_next_open_row(board, col):
# #     for r in range(ROW_COUNT):
# #         if board[r][col] == -1:
# #             return r

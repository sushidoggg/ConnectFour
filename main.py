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
from player import AIPlayer, RandomPlayer

import time
import sys
import math
import pygame
from interface import draw_window, Button, drop_piece, is_valid_location, draw_one_disc, print_win, draw_hint_disc

from connect_four import ConnectFour

pygame.init()  # pygame needs to be initialized before defining FONT

from interface import SQUARESIZE, COLOR_PLAYER_ONE, COLOR_PLAYER_TWO, BLUE, WHITE, \
    BLACK, PLAYER_ONE, PLAYER_TWO, SIZE, FONT_WORDS, FONT_WIN_STATUS, UNOCCUPIED, AI_RESPONSE_TIME


connect_four_game = ConnectFour()

screen = pygame.display.set_mode(SIZE)
pygame.display.flip()

user_go_first = None
AI_player = None

game_status = 'before_game'


# create all the button
hint_button = Button(x=10 * SQUARESIZE, y=6 * SQUARESIZE, word='HINT')
restart_button = Button(x=10 * SQUARESIZE, y=8 * SQUARESIZE, word='RESTART')
go_first_button = Button(x=10 * SQUARESIZE, y=2 * SQUARESIZE, word='I go first')
go_second_button = Button(x=10 * SQUARESIZE, y=4 * SQUARESIZE, word='AI go first')
buttons = [hint_button, restart_button, go_first_button, go_second_button]
draw_window(screen, connect_four_game, [hint_button, restart_button, go_first_button, go_second_button])
clock = pygame.time.Clock()
while True:
    # print(game_status)
    if game_status == 'before_game':
        print('restarted')
        connect_four_game = ConnectFour()
        # activate two modes buttons and de-activate the other two
        go_first_button.reset_disabled(False)
        go_second_button.reset_disabled(False)
        restart_button.reset_disabled(True)
        hint_button.reset_disabled(True)
        pygame.display.set_caption("CONNECT FOUR - PLAY AGAINST AI")
        draw_window(screen, connect_four_game, buttons)
        label_choose_order = FONT_WORDS.render("Choose if you want to go first or last!", True, BLACK)
        screen.blit(label_choose_order, (SQUARESIZE, SQUARESIZE))
        pygame.display.update()

        user_go_first = None
        position = (0, 0)  # initialize the position
        while (not go_first_button.is_valid(position, screen)) and (not go_second_button.is_valid(position, screen)):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = event.pos
                elif event.type == pygame.QUIT:
                    sys.exit()

        if go_first_button.is_valid(position, screen):
            user_go_first = True
            # AI_player = RandomPlayer(2)
            AI_player = AIPlayer(PLAYER_TWO, 5, None)
            # AI_player = AIPlayer(PLAYER_TWO, 5, None)
        else:
            user_go_first = False
            # AI_player = AIPlayer(PLAYER_ONE, 5, None)
            AI_player = AIPlayer(PLAYER_ONE, 5, None)
            # AI_player = RandomPlayer(2)
        go_second_button.reset_disabled(True)
        go_first_button.reset_disabled(True)
        restart_button.reset_disabled(False)
        hint_button.reset_disabled(False)
        draw_window(screen, connect_four_game, buttons)

        game_status = 'gaming'
    elif game_status == 'gaming':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, WHITE, (0.5 * SQUARESIZE, SQUARESIZE, 8.5 * SQUARESIZE, SQUARESIZE))
                posx, posy = event.pos[0], event.pos[1]
                if SQUARESIZE <= posx <= 8 * SQUARESIZE and SQUARESIZE <= posy <= 8 * SQUARESIZE and user_go_first:  # posx, posy in the region for selection and player is user :
                    draw_one_disc(screen, COLOR_PLAYER_ONE, (posx, int(SQUARESIZE / 2 + SQUARESIZE)))
                elif SQUARESIZE <= posx <= 8 * SQUARESIZE and SQUARESIZE <= posy <= 8 * SQUARESIZE and not user_go_first:
                    draw_one_disc(screen, COLOR_PLAYER_TWO, (posx, int(SQUARESIZE / 2 + SQUARESIZE)))
                pygame.display.update()


            if event.type == pygame.MOUSEBUTTONDOWN and user_go_first:
                posx, posy = event.pos[0], event.pos[1]
                # if player click on the board
                if SQUARESIZE <= posx <= 8 * SQUARESIZE and SQUARESIZE <= posy <= 8 * SQUARESIZE:
                    col = int(math.floor(posx / SQUARESIZE) - 1)
                    valid = is_valid_location(connect_four_game, col)
                    if valid:
                        drop_piece(connect_four_game, col)
                        draw_window(screen, connect_four_game, buttons)
                        if connect_four_game.get_winner() is not None:
                            game_status = 'game_over'
                            break
                        # AI's turn
                        clock.tick(AI_RESPONSE_TIME)
                        col_AI = AI_player.choose_column(connect_four_game)
                        drop_piece(connect_four_game, col_AI)
                        draw_window(screen, connect_four_game, buttons)

                        if connect_four_game.get_winner() is not None:
                            game_status = 'game_over'
                            break
                    else:
                        label_not_valid = FONT_WORDS.render("Choose another column!", True, BLACK)
                        screen.blit(label_not_valid, (SQUARESIZE, SQUARESIZE))
                        pygame.display.update()
                elif hint_button.is_valid(event.pos, screen):  # player click HINT button:
                    col = AI_player.hint_opponent(connect_four_game)
                    draw_hint_disc(screen, col, connect_four_game)
                elif restart_button.is_valid(event.pos, screen):
                    game_status = 'before_game'
                    break
            elif not user_go_first:  # AI goes first
                if connect_four_game.get_current_player() == PLAYER_ONE:  # if it's AI's turn
                    clock.tick(AI_RESPONSE_TIME)
                    col_AI = AI_player.choose_column(connect_four_game)
                    drop_piece(connect_four_game, col_AI)
                    draw_window(screen, connect_four_game, buttons)

                    if connect_four_game.get_winner() is not None:
                        game_status = 'game_over'
                        break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx, posy = event.pos[0], event.pos[1]
                    # if player click the board
                    if SQUARESIZE <= posx <= 8 * SQUARESIZE and SQUARESIZE <= posy <= 8 * SQUARESIZE:
                        # if connect_four_game.get_current_player() == PLAYER_TWO:
                        col = int(math.floor(posx / SQUARESIZE) - 1)
                        valid = is_valid_location(connect_four_game, col)
                        if valid:
                            drop_piece(connect_four_game, col)
                            draw_window(screen, connect_four_game, buttons)
                            if connect_four_game.get_winner() is not None:
                                game_status = 'game_over'
                                break
                        else:
                            print("NOT VALID")
                            label_not_valid = FONT_WORDS.render("Choose another column!", True, BLACK)
                            screen.blit(label_not_valid, (SQUARESIZE, SQUARESIZE))
                            pygame.display.update()
                    elif hint_button.is_valid(event.pos, screen):  # player click HINT button:
                        col = AI_player.hint_opponent(connect_four_game)
                        draw_hint_disc(screen, col, connect_four_game)
                    elif restart_button.is_valid(event.pos, screen):
                        game_status = 'before_game'
                        break

    elif game_status == 'game_over':
        if (connect_four_game.get_winner() == PLAYER_ONE and user_go_first) or \
                (connect_four_game.get_winner() == PLAYER_TWO and not user_go_first):
            print_win(screen, 'You Win!')
        elif connect_four_game.get_winner() == UNOCCUPIED:
            print_win(screen, 'TIE!')
        else:
            print_win(screen, 'AI Win!')
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if restart_button.is_valid(event.pos, screen):
                    game_status = 'before_game'
                    break

    else:
        print('Invalid game_status')
    print('ONE WHILE LOOP')
    clock.tick(200)

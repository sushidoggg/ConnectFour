from __future__ import annotations

import sys
import math
import pygame
from interface import draw_window

from connect_four import ConnectFour

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE= 75
RADIUS = int(SQUARESIZE / 3)
WINDOW_WIDTH, WINDOW_HEIGHT = SQUARESIZE * 11, SQUARESIZE * 11
SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

BUTTOM_COLUMN_WIDTH = ...
FONT = pygame.font.SysFont("monospace", 75)
COLOR_PLAYER_ONE, COLOR_PLAYER_TWO = (0, 255, 255), (255, 0, 0)
BLUE, WHITE, BLACK = (0, 0, 255), (255, 255, 255), (0,0,0)

connect_four_game = ConnectFour()
game_over = False

pygame.init()
screen = pygame.display.set_mode(SIZE)



draw_window(screen, connect_four_game)
pygame.display.update()


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen,BLACK,(SQUARESIZE, SQUARESIZE, 7*SQUARESIZE, SQUARESIZE))
            posx, posy = event.pos[0], event.pos[1]
            if #posx, posy in the region for selection and player is user :
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2 + SQUARESIZE)), RADIUS) #Olivia 改一下颜色
            else:
                pass

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            posx, posy = event.pos[0], event.pos[1]
            if posx in [SQUARESIZE, 8 * SQUARESIZE] and posy in [SQUARESIZE, 8 * SQUARESIZE]:
                # making a selection on game board
                # ask player 1 input
                if connect_four_game.get_current_player() == 0:
                    if #player 1 is user: #TODO
                        col = int(math.floor(posx/SQUARESIZE) - 1)

                        # col = int(input("Player 1 Make your selection: (0, 6)"))
                        if is_valid_location(connect_four_game.grid, col):
                            row = get_next_open_row(connect_four_game.grid, col)
                            drop_piece(connect_four_game.grid, row, col, 0)
                    else:
                        # AI moves #TODO

                # ask player 2 input
                else:  # player 2 turn
                    if 1>2: #player 1 is user: #TODO
                        #AI moves #TODO
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

if connect_four_game.get_winner() #是user的话：
    label = FONT.render("You win!", TRUE, RED)
else:
    label = FONT.render("AI wins!", TRUE, RED)
screen.blit(lable, (SQUARESIZE + 40, 10))


def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    # check if the location is valid
    return board[ROW_COUNT - 1][col] == -1

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == -1:
            return r

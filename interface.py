"""CSC111 Winter 2023 Project: Connect 4 (Interface)

Module Description
==================

This module contains a collection of Python classes and functions that represent the interface of Connect 4,
which is mainly implemented using the Pygame modules.
By reading the *docstring* of this file, you can gain insights into the
role and functionality of these classes and functions as well as how they contribute to this project as a whole.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the
Teaching Stream of CSC111 at the University of Toronto St. George campus.
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2023 Yige (Amanda) Wu, Sunyi (Alysa) Liu, Lecheng (Joyce) Qu, and Xi (Olivia) Yan.
"""
from __future__ import annotations
from connect_four import ConnectFour
import pygame

SQUARESIZE= 75
RADIUS = int(SQUARESIZE / 3)
WINDOW_WIDTH, WINDOW_HEIGHT = SQUARESIZE * 11, SQUARESIZE * 11
BUTTOM_COLUMN_WIDTH = ...
FONT = ...
COLOR_PLAYER_ONE, COLOR_PLAYER_TWO = (0, 255, 255), (255, 0, 0)
BLUE, WHITE, BLACK = (0, 0, 255), (255, 255, 255), (0,0,0)
ROW_COUNT, COLUMN_COUNT = 6, 7

def draw_board(window: pygame.Surface) -> None:
    '''Based on the given sqaure size, draw an interface that has a 6*7 board on the given window'''
    window.fill(WHITE)
    pygame.display.flip()
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(window, BLUE, ((c + 1)* SQUARESIZE, (r + 2) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(window, WHITE, (
                int((c + 1) * SQUARESIZE + SQUARESIZE / 2), int((r + 2) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

# 模拟main里面的window
pygame.display.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Connect Four")
# main while loop
def draw_window(window: pygame.Surface, game: ConnectFour):
    draw_board(window)
    # draw a disc based on who plays and the positon
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()





class Disc():
    '''A class that represents the disc that players played
    Instance Attributes:
        - position: list[tuple]
        - color: list[tuple]
    Representation Invariants:
        - color in {COLOR_PLAYER_TWO, COLOR_PLAYER_ONE}'''
    ...

class Player(pygame.sprite.Sprite):
    '''A class that represents Player.
    # todo：return the column int player choose'''
    ...

class AI(pygame.sprite.Sprite):
    ...
def events_simulator(game: ConnectFour):
    '''Run events while not game_over. Use event.handle_events(ConnectFour)
    Preconditions:
        - ConnectFour.first_player_moves is empty'''


def is_valid_position() -> bool:
# return the user's move as an integer to connect_four.py.
    ...

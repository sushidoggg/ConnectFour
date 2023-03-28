import pygame
from __future__ import annotations

SQUARESIZE = ...
BOARD_WIDTH, BOARD_HEIGHT = SQUARESIZE * 7, SQUARESIZE * (6 + 1)
BUTTOM_COLUMN_WIDTH =
SCREEN_WIDTH, SCREEN_HEIGHT = BOARD_WIDTH + ..., BOARD_HEIGHT
FONT = ...
COLOR_PLAYER_ONE, COLOR_PLAYER_TWO = (0, 255, 255), (255, 0, 0)

class Disc():
    '''A class that represents the disc that players played
    Instance Attributes:
        - position: list[tuple]
        - color: list[tuple]
    Representation Invariants:
        - color in {COLOR_PLAYER_TWO, COLOR_PLAYER_ONE}'''


class Player(pygame.sprite.Sprite):
    '''A class that represents Player.
    # todo：return the column int player choose'''

class AI(pygame.sprite.Sprite):
    ...
def draw_window(sqau re_size: int) -> pygame.Surface:
    '''Based on the given sqaure size, draw an interface that has a 6*7 board, buttons on the right'''
    ...

def events_simulator(game: ConnectFour):
    '''Run events while not game_over. Use event.handle_events(ConnectFour)
    Preconditions:
        - ConnectFour.first_player_moves is empty'''


def is_valid_position() -> bool:
# return the user's move as an integer to connect_four.py.

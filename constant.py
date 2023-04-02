"""
# TODO
"""
import pygame

GAME_NOT_STARTED, GAMING, GAME_OVER = -1, 0, 1
GAME_START_MOVE = "*"

UNOCCUPIED, PLAYER_ONE, PLAYER_TWO, HINT = -1, 0, 1, 2
ORIENTATIONS = ((0, 1), (1, 0), (1, 1), (1, -1))    # Horizontal, vertical, two diagonal

SQUARESIZE = 70
RADIUS = int(SQUARESIZE / 3.5)

GRID_WIDTH, GRID_HEIGHT = 7, 6
WINDOW_WIDTH, WINDOW_HEIGHT = SQUARESIZE * 11, SQUARESIZE * 11
BORDER_RADIUS = int(SQUARESIZE / 3.5)
BUTTON_WIDTH, BUTTON_HEIGHT = int(SQUARESIZE * 1.5), int(SQUARESIZE * 0.7)

RED, YELLOW = (255, 71, 71), (255, 196, 0)
DARK_RED, DARK_YELLOW = (178, 49, 49), (178, 137, 0)
BLUE, WHITE, BLACK, GREY = (65, 108, 234), (255, 255, 255), (0, 0, 0), (192, 192, 192)
LIGHT_BLUE, DARK_BLUE, DARK_GREY = (97, 162, 255), (45, 75, 163), (134, 134, 134)

pygame.init()
FONT_WORDS = pygame.font.SysFont("Courier", int(SQUARESIZE/3))
FONT_WIN_STATUS = pygame.font.SysFont("Courier", int(SQUARESIZE/1.5))
FONT_SIZE = int(SQUARESIZE / 2.5)
FONT_BUTTON = pygame.font.Font(None, FONT_SIZE)

if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

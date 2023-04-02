"""CSC111 Winter 2023 Project: Connect 4 (Constant)

Module Description
==================

This module contains all the constants defined that are essential for implementing
the Connect 4 game. These are the constants defined for all the functions we created
including the implementation of the game itself and the pygame interface.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the
Teaching Stream of CSC111 at the University of Toronto St. George campus.
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2023 Yige (Amanda) Wu, Sunyi (Alysa) Liu, Lecheng (Joyce) Qu, and Xi (Olivia) Yan.
"""
import pygame

# Representations
GAME_START_MOVE = "*"
GAME_NOT_STARTED, GAMING, GAME_OVER = -1, 0, 1
UNOCCUPIED, PLAYER_ONE, PLAYER_TWO, HINT = -1, 0, 1, 2

GRID_WIDTH, GRID_HEIGHT = 7, 6

ORIENTATIONS = ((0, 1), (1, 0), (1, 1), (1, -1))    # Horizontal, vertical, two diagonal

# Window sizes
# We try to compute all sizes and coordinates according to SQUARESIZE, so that we can modify
# the size of the window if we want to.
SQUARESIZE = 70
RADIUS = int(SQUARESIZE / 3.5)
WINDOW_WIDTH, WINDOW_HEIGHT = SQUARESIZE * 11, SQUARESIZE * 11
BORDER_RADIUS = int(SQUARESIZE / 3.5)
BUTTON_WIDTH, BUTTON_HEIGHT = int(SQUARESIZE * 1.5), int(SQUARESIZE * 0.7)

# Colors
RED, YELLOW = (255, 71, 71), (255, 196, 0)
DARK_RED, DARK_YELLOW = (178, 49, 49), (178, 137, 0)
BLUE, WHITE, BLACK, GREY = (65, 108, 234), (255, 255, 255), (0, 0, 0), (192, 192, 192)
LIGHT_BLUE, DARK_BLUE, DARK_GREY = (97, 162, 255), (45, 75, 163), (134, 134, 134)

pygame.init()
# We disabled python_ta's 'forbidden-top-level-code' error, because we need pygame.init() to be able to
# define the fonts as global variables, due to the constraints of pygame.
# Also, python_ta can't recognize that pygame has and init function, so we also disabled 'no-member'.

# Fonts
FONT_WORDS = pygame.font.SysFont("Courier", SQUARESIZE // 3)
FONT_WIN_STATUS = pygame.font.SysFont("Courier", int(SQUARESIZE / 1.5))
FONT_SIZE = int(SQUARESIZE / 2.5)
FONT_BUTTON = pygame.font.Font(None, FONT_SIZE)

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'max-nested-blocks': 4,
        'extra-imports': ['pygame'],
        'disable': ['no-member', 'forbidden-top-level-code'],
    })

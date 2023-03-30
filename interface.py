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
from main import SQUARESIZE, RADIUS, WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_PLAYER_ONE, COLOR_PLAYER_TWO, BLUE, WHITE, \

    BLACK, ROW_COUNT, COLUMN_COUNT, FONT
import pygame

# todo: I NEED a FONT that can be used

BUTTON_WIDTH, BUTTON_HEIGHT = SQUARESIZE * 0.7, SQUARESIZE * 0.7
DISABLE_COLOR = (100,100,100) # Grey
BUTTON_COLOR = COLOR_PLAYER_ONE

class Button():
    """A class represents a circle buttons."""
    word: str
    center: tuple[int, int]
    clicked: bool
    def __init__(self, x: int, y: int, word: str) -> None:
        """Create a rectangular button of given image at (x, y)
        x, y are the topleft location of the button on a screen.
        image is the location of the image on the button. The image's size should match BUTTON_WIDETH and BUTTON_HEIGHT in the same ratio"""

        # img = pygame.image.load(image).convert_alpha()
        # self.image = pygame.transform.scale(img, (BUTTON_WIDTH, BUTTON_HEIGHT))
        self.center = (x, y)
        self.word = word
        self.clicked = False

    def draw(self, window: pygame.Surface) -> None:
        """Draw the button with words on it on the given window. """
        # draw a rectangle
        topleft_x = int(self.center[0] - BUTTON_WIDTH / 2)
        topleft_y = int(self.center[1] - BUTTON_HEIGHT / 2)
        pygame.draw.rect(window, BUTTON_COLOR, (topleft_x, topleft_y, BUTTON_WIDTH, BUTTON_HEIGHT))
        # draw word
        text = FONT.render(self.word, True, BLACK) # todo: change the font
        w, h = text.get_size()
        text_x = int(self.center[0] - w / 2)
        text_y = int(self.center[1] - h / 2)
        window.blit(text, (text_x, text_y))
        pygame.display.update()

    def disabled(self, window: pygame.Surface) -> None:
        """Make the button grey color"""
        # draw a rectangle
        topleft_x = int(self.center[0] - BUTTON_WIDTH / 2)
        topleft_y = int(self.center[1] - BUTTON_HEIGHT / 2)
        pygame.draw.rect(window, DISABLE_COLOR, (topleft_x, topleft_y, BUTTON_WIDTH, BUTTON_HEIGHT))
        # draw word
        text = FONT.render(self.word, True, BLACK) # todo: change the font
        w, h = text.get_size()
        text_x = int(self.center[0] - w / 2)
        text_y = int(self.center[1] - h / 2)
        window.blit(text, (text_x, text_y))
        pygame.display.update()

    def is_valid(self, position: tuple[int]) -> bool:
        left, right = int(self.center[0] - BUTTON_WIDTH / 2), int(self.center[0] + BUTTON_WIDTH / 2)
        up, down = int(self.center[1] - BUTTON_HEIGHT / 2), int(self.center[1] + BUTTON_HEIGHT / 2)
        if left <= position[0] <= right and up <= position[1] <= down:
            self.clicked = True
            # todo：做一个按下去的动画
            return True
        else:
            return False


def draw_one_disc(window: pygame.Surface, color: tuple[int, int, int], center: tuple[int, int]) -> None:
    """Draw a beautiful disc on window at the given window with given color"""
    ...
    pygame.draw.circle(window, color, (center[0], center[1]), RADIUS)
    # create a darker color and draw the outer circle of the disc
    darker = (int(color[0] / 3), int(color[1] / 3), int(color[2] / 3))
    pygame.draw.circle(window, darker, (center[0], center[1]), RADIUS, int(RADIUS / 5))
    pygame.display.update()



def draw_window(window: pygame.Surface, game: ConnectFour) -> None:
    """Based on the given sqaure size, draw the whole interface on the given window at the current status of game
        If game.grid are all unoccupied, then just draw the window"""
    window.fill(WHITE)
    pygame.display.flip()
    grid = game.grid
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(window, BLUE, ((c + 1) * SQUARESIZE, (r + 2) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(window, WHITE, (
                int((c + 1) * SQUARESIZE + SQUARESIZE / 2), int((r + 2) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # TODO: convert grid-index to pygame's index
            if grid[r][c] == 1:  # Player Two's disc
                pygame.draw.circle(window, COLOR_PLAYER_TWO, (
                    int((c + 1) * SQUARESIZE + SQUARESIZE / 2), int((r + 2) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif grid[r][c] == 0:  # Player One's disc
                pygame.draw.circle(window, COLOR_PLAYER_ONE, (
                    int((c + 1) * SQUARESIZE + SQUARESIZE / 2), int((r + 2) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


def drop_piece(game: ConnectFour, col: int) -> None:
    """
    Represent the player's move on the board.
    """
    # board[row][col] = piece
    game.record_player_move(col)


def is_valid_location(game: ConnectFour, col: int) -> bool:
    """
    Return if the current column is a valid column.
    """
    # return board[ROW_COUNT - 1][col] == -1
    return col in game.get_possible_columns()


# def get_next_open_row(game: ConnectFour, col: int) -> int:
#     """
#     Get the next avaible row position for the current column.
#     """
#     # for r in range(ROW_COUNT):
#     #     if board[r][col] == -1:
#     #         return r
#     return game.get_move_position_by_column(col)[0]




if __name__ == '__main__':
    # 模拟main里面的window
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    window.fill((0,0,0))
    pygame.display.set_caption("Connect Four")
    pygame.display.flip()
    b1 = Button(100, 100, "Heelo")
    b1.draw(window)
    pygame.display.update()

    # main while loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

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
    BLACK, ROW_COUNT, COLUMN_COUNT
import pygame


BUTTON_WIDTH, BUTTON_HEIGHT = SQAURESIZE * 0.7, SQAURESIZE * 0.7
# todo: click the two buttons and see if it is user
class Button():
    """A class represents a circle buttons."""
    image: pygame.Surface
    rect: pygame.Rect
    clicked: bool
    def __init__(self, x: int, y: int, image: str) -> None:
        """Create a button of given image at (x, y)"""
        img = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(img, (BUTTON_WIDTH, BUTTON_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    def draw(self, window: pygame.Surface) -> bool:
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        # draw button on screen
        window.blit(self.image, (self.rect.x, self.rect.y))

        return action


def draw_one_disc(window: pygame.Surface, color: tuple[int], center: tuple[int]) -> None:
    """Draw a beautiful disc on window at the given window with given color"""
    ...


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

    pygame.display.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Connect Four")
    # main while loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

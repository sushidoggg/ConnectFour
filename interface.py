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
from typing import Optional
import pygame
from pygame import gfxdraw
from connect_four import ConnectFour

AI_RESPONSE_TIME = 50
UNOCCUPIED, PLAYER_ONE, PLAYER_TWO, HINT = -1, 0, 1, 2
GRID_WIDTH, GRID_HEIGHT = 7, 6

SQUARESIZE = 70
RADIUS = int(SQUARESIZE / 3.5)

WINDOW_WIDTH, WINDOW_HEIGHT = SQUARESIZE * 11, SQUARESIZE * 11
SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
BORDER_RADIUS = int(SQUARESIZE / 3.5)

RED, YELLOW = (255, 71, 71), (255, 196, 0)
DARK_RED, DARK_YELLOW = (178, 49, 49), (178, 137, 0)
BLUE, WHITE, BLACK, GREY = (65, 108, 234), (255, 255, 255), (0, 0, 0), (192, 192, 192)
LIGHT_BLUE, DARK_BLUE, DARK_GREY = (97, 162, 255), (45, 75, 163), (134, 134, 134)
BUTTON_WIDTH, BUTTON_HEIGHT = int(SQUARESIZE * 1.5), int(SQUARESIZE * 0.7)

pygame.init()
FONT_WORDS = pygame.font.SysFont("Courier", int(SQUARESIZE/3))
FONT_WIN_STATUS = pygame.font.SysFont("Courier", int(SQUARESIZE/1.5))
FONT_SIZE = int(SQUARESIZE / 2.5)
FONT_BUTTON = pygame.font.Font(None, FONT_SIZE)


class Button:
    """A class represents a circle buttons.
    Instance Attributes:
        - disabled: show that if the button should be disactivated, this attribute needs to be changed manually
        - word: the word that is printed on the button
        - center: a tuple of integers that is the center location of the button
    """
    word: str
    center: tuple[int, int]
    disabled: bool
    _button_color: tuple[int, int, int]
    _darker_button_color: tuple[int, int, int]
    _disabled_color: tuple[int, int, int]

    def __init__(self, x: int, y: int, word: str) -> None:
        """Create a rectangular button of given image at (x, y)
        x, y are the topleft location of the button on a surface.
        image is the location of the image on the button. The image's size should match BUTTON_WIDETH and BUTTON_HEIGHT
        in the same ratio
        """
        self.center = (x, y)
        self.word = word
        self.disabled = False

        self._button_color = BLUE
        self._darker_button_color = DARK_BLUE
        self._disabled_color = GREY

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the button with words on it on the given window.
        It doesn't update surface in this function."""

        # draw a rectangle
        topleft_x = int(self.center[0] - BUTTON_WIDTH / 2)
        topleft_y = int(self.center[1] - BUTTON_HEIGHT / 2)

        if self.disabled:
            filled_color, outline_color = self._disabled_color, self._disabled_color
        else:
            filled_color, outline_color = self._button_color, self._darker_button_color

        # draw the outer Rect
        draw_rounded_rect(surface, pygame.Rect(topleft_x, topleft_y, BUTTON_WIDTH, BUTTON_HEIGHT),
                          outline_color, BORDER_RADIUS)
        # draw the inner Rect
        draw_rounded_rect(surface, pygame.Rect(topleft_x + int(BUTTON_WIDTH * 0.05),
                                               topleft_y + int(BUTTON_WIDTH * 0.05),
                          int(BUTTON_WIDTH * 0.9), int(0.85 * BUTTON_HEIGHT)),
                          filled_color, int(BORDER_RADIUS * 0.8))

        # draw word
        text = FONT_BUTTON.render(self.word, True, WHITE)
        w, h = text.get_size()
        text_x, text_y = int(self.center[0] - w / 2), int(self.center[1] - h / 2)
        surface.blit(text, (text_x, text_y))

    def is_valid_click(self, position: tuple[int, int]) -> bool:
        """Return if the given position is on the position of the button
        Doesn't mutate self.disabled
        Precondition:
            - 0 <= position[0] <= WINDOW_WIDTH
            - 0 <= position[1] <= WINDOW_HEIGHT
        """
        if self.disabled:
            return False

        left, right = int(self.center[0] - BUTTON_WIDTH / 2), int(self.center[0] + BUTTON_WIDTH / 2)
        up, down = int(self.center[1] - BUTTON_HEIGHT / 2), int(self.center[1] + BUTTON_HEIGHT / 2)
        if left <= position[0] <= right and up <= position[1] <= down:
            return True
        else:
            return False


class GameBoard:
    """
    ...
    """
    x: int
    y: int
    _grid: list[list[Disc]]
    _hint_position: Optional[tuple[int, int]]

    def __init__(self, x: int, y: int) -> None:
        """
        ...
        """
        self.x, self.y = x, y
        self._grid = []
        for grid_y in range(GRID_HEIGHT):
            row_so_far = []
            for grid_x in range(GRID_WIDTH):
                position_x, position_y = self._get_central_position(grid_x, grid_y)
                row_so_far.append(Disc(position_x, position_y, UNOCCUPIED))
            self._grid.append(row_so_far)
        self._hint_position = None

    def _get_central_position(self, grid_x: int, grid_y: int) -> tuple[int, int]:
        """
        # TODO
        """
        position_x = int(self.x + (grid_x + 0.5) * SQUARESIZE)
        position_y = int(self.y + (grid_y + 0.5) * SQUARESIZE)
        return (position_x, position_y)

    def draw(self, surface: pygame.Surface) -> None:
        """
        ...
        """
        board_rect = pygame.Rect(self.x, self.y, GRID_WIDTH * SQUARESIZE, GRID_HEIGHT * SQUARESIZE)
        draw_rounded_rect(surface, board_rect, BLUE, BORDER_RADIUS)

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                self._grid[y][x].draw(surface)

    def is_valid_click(self, position: tuple[int, int]) -> bool:
        """
        ...
        """
        position_x, position_y = position
        return self.x <= position_x <= self.x + SQUARESIZE * GRID_WIDTH and \
            self.y <= position_y <= self.y + SQUARESIZE * GRID_HEIGHT

    def get_move_column(self, position: tuple[int, int]) -> int:
        """
        ...
        """
        return (position[0] - self.x) // SQUARESIZE

    def record_move(self, move_position: tuple[int, int], disc_type) -> None:
        """
        ...
        """
        x, y = move_position
        y = GRID_HEIGHT - 1 - y     # TODO
        self._grid[y][x].update_color_and_type(disc_type)
        if disc_type == HINT:
            self._hint_position = (x, y)

    def remove_hint(self) -> None:
        """
        ...
        """
        if self._hint_position is not None:
            x, y = self._hint_position
            self._grid[y][x].update_color_and_type(UNOCCUPIED)


class Disc:
    """
    ...
    """
    x: int
    y: int
    disc_type: int
    filled_color: tuple[int, int, int]
    outline_color: tuple[int, int, int]

    def __init__(self, x: int, y: int, disc_type: int) -> None:
        """
        ...
        """
        self.x, self.y = x, y
        self.update_color_and_type(disc_type)

    def draw(self, surface: pygame.Surface) -> None:
        """
        ...
        """
        draw_circle(surface, self.x, self.y, RADIUS, self.outline_color)
        draw_circle(surface, self.x, self.y, int(RADIUS * 4 / 5), self.filled_color)

    def update_color_and_type(self, disc_type) -> None:
        """
        ...
        """
        self.disc_type = disc_type
        if self.disc_type == UNOCCUPIED:
            self.filled_color, self.outline_color = WHITE, WHITE
        elif self.disc_type == PLAYER_ONE:
            self.filled_color, self.outline_color = RED, DARK_RED
        elif self.disc_type == PLAYER_TWO:
            self.filled_color, self.outline_color = YELLOW, DARK_YELLOW
        else:
            self.filled_color, self.outline_color = GREY, DARK_GREY


class Label:
    """
    ...
    """
    x: int
    y: int
    text: pygame.Surface
    font: pygame.font.Font
    color: tuple[int, int, int]
    visible: bool
    background_rect: Optional[pygame.Rect]
    background_color: Optional[tuple[int, int, int]]
    align: str

    def __init__(self, x: int, y: int, text: str, font: pygame.font.Font, color: tuple[int, int, int],
                 background_rect: Optional[pygame.Rect] = None,
                 background_color: Optional[tuple[int, int, int]] = None, visible: bool = True,
                 align: str = 'center') -> None:
        """
        ...
        """
        self.x, self.y = x, y   # Center x, Center y
        self.font, self.color = font, color
        self.update_text(text)
        self.visible = visible
        self.background_rect, self.background_color = background_rect, background_color
        self.align = align

    def draw(self, surface: pygame.Surface) -> None:
        """
        ...
        """
        if not self.visible:
            return
        if self.background_rect is not None:
            pygame.draw.rect(surface, self.background_color, self.background_rect)

        if self.align == 'center':
            text_rect = self.text.get_rect(center=(self.x, self.y))
            surface.blit(self.text, text_rect)
        elif self.align == 'left':
            surface.blit(self.text, (self.x, self.y))

    def update_text(self, text: str) -> None:
        """
        ...
        """
        self.text = self.font.render(text, True, self.color)


def draw_circle(surface, x, y, radius, color) -> None:
    """
    Draw an anti-aliased circle at the position (x, y) given the radius and color
    """
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)


def draw_rounded_rect(surface: pygame.Surface, rect: pygame.Rect, color: tuple[int, int, int], corner_radius: int) -> \
        None:
    """Draw an anti-aliased rectangle with rounded corners. We draw anti-aliased circles at the corners
    Would prefer this:
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
    """
    # draw four anti aliasing circles to smooth the corners
    # top left
    draw_circle(surface, rect.left + corner_radius, rect.top + corner_radius, corner_radius, color)
    # top right
    draw_circle(surface, rect.right - corner_radius - 1, rect.top + corner_radius, corner_radius, color)
    # bottom left
    draw_circle(surface, rect.left + corner_radius, rect.bottom - corner_radius - 1, corner_radius, color)
    # bottom right
    draw_circle(surface, rect.right - corner_radius - 1, rect.bottom - corner_radius - 1, corner_radius, color)

    rect_tmp = pygame.Rect(rect)
    rect_tmp.width -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)

    rect_tmp.width = rect.width
    rect_tmp.height -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)

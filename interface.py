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
import pygame
import time
from connect_four import ConnectFour

UNOCCUPIED, PLAYER_ONE, PLAYER_TWO = -1, 0, 1
ROW_COUNT, COLUMN_COUNT = 6, 7
SQUARESIZE = 70
RADIUS = int(SQUARESIZE / 3.5)
WINDOW_WIDTH, WINDOW_HEIGHT = SQUARESIZE * 11, SQUARESIZE * 11
SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
BORDER_RADIUS = int(SQUARESIZE / 4)
pygame.init()
BUTTOM_COLUMN_WIDTH = ...
COLOR_PLAYER_ONE, COLOR_PLAYER_TWO = (255, 71, 71), (255, 196, 0)
BLUE, WHITE, BLACK = (65, 108, 234), (255, 255, 255), (0, 0, 0)
BUTTON_WIDTH, BUTTON_HEIGHT = int(SQUARESIZE * 1.5) , int(SQUARESIZE * 0.7)
DISABLE_COLOR = (192, 192, 192)  # Grey
BUTTON_COLOR = BLUE
pygame.init()

FONT_WORDS = pygame.font.SysFont("Courier", int(SQUARESIZE/3))
FONT_WIN_STATUS = pygame.font.SysFont("Courier", int(SQUARESIZE/1.5))
FONT_SIZE = int(SQUARESIZE / 2.5)
FONT_BUTTON = pygame.font.Font(None, FONT_SIZE)


class Button():
    """A class represents a circle buttons.
    Instance Attributes:
        - disabled: show that if the button should be disactivated, this attribute needs to be changed manually
        - word: the word that is printed on the button
        - center: a tuple of integers that is the center location of the button
    """
    word: str
    center: tuple[int, int]
    disabled: bool
    def __init__(self, x: int, y: int, word: str) -> None:
        """Create a rectangular button of given image at (x, y)
        x, y are the topleft location of the button on a screen.
        image is the location of the image on the button. The image's size should match BUTTON_WIDETH and BUTTON_HEIGHT in the same ratio"""
        self.center = (x, y)
        self.word = word
        self.disabled = False

    def draw(self, window: pygame.Surface) -> None:
        """Draw the button with words on it on the given window.
        It doesn't update screen in this function"""
        # draw a rectangle
        topleft_x = int(self.center[0] - BUTTON_WIDTH / 2)
        topleft_y = int(self.center[1] - BUTTON_HEIGHT / 2)
        pygame.draw.rect(window, BUTTON_COLOR, (topleft_x, topleft_y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=BORDER_RADIUS)
        darker = (int(BUTTON_COLOR[0] * 0.7), int(BUTTON_COLOR[1] * 0.7), int(BUTTON_COLOR[2] * 0.7))
        pygame.draw.rect(window, darker, (topleft_x, topleft_y, BUTTON_WIDTH, BUTTON_HEIGHT), 4, border_radius=BORDER_RADIUS)
        # draw word
        text = FONT_BUTTON.render(self.word, True, WHITE)
        w, h = text.get_size()
        text_x = int(self.center[0] - w / 2)
        text_y = int(self.center[1] - h / 2)
        window.blit(text, (text_x, text_y))
        # pygame.display.update()

    def show_disabled(self, window: pygame.Surface) -> None:
        """Make the button to a grey color
        It doesn't update screen in this function
        Representation Invariants:
            - self.disabled is True
        """
        # draw a rectangle
        topleft_x = int(self.center[0] - BUTTON_WIDTH / 2)
        topleft_y = int(self.center[1] - BUTTON_HEIGHT / 2)
        pygame.draw.rect(window, DISABLE_COLOR, (topleft_x, topleft_y, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=BORDER_RADIUS)
        # draw word
        text = FONT_BUTTON.render(self.word, True, BLACK)
        w, h = text.get_size()
        text_x = int(self.center[0] - w / 2)
        text_y = int(self.center[1] - h / 2)
        window.blit(text, (text_x, text_y))

    def is_valid(self, position: tuple[int, int], window: pygame.Surface) -> bool:
        """Return if the given position is on the position of the button
        Doesn't mutate self.disabled
        Precondition:
            - 0 <= position[0] <= WINDOW_WIDTH
            - 0 <= position[1] <= WINDOW_HEIGHT
        """
        left, right = int(self.center[0] - BUTTON_WIDTH / 2), int(self.center[0] + BUTTON_WIDTH / 2)
        up, down = int(self.center[1] - BUTTON_HEIGHT / 2), int(self.center[1] + BUTTON_HEIGHT / 2)
        if left <= position[0] <= right and up <= position[1] <= down:
            self.show_disabled(window)
            pygame.display.update()
            time.sleep(0.2)
            self.draw(window)
            pygame.display.update()
            return True
        else:
            return False

    def reset_disabled(self, value: bool) -> None:
        """Change self.disabled to the given boolean value"""
        self.disabled = value


def draw_one_disc(window: pygame.Surface, color: tuple[int, int, int], center: tuple[int, int]) -> None:
    """Draw a beautiful disc on window at the given window with given color
        The disc has two layers, color is its inner/base color; a darker color is its outer color
        Preconditions:
            - 0 <= center[0] <= WINDOW_WIDTH and 0 <= center[1] <= WINDOW_HEIGHT
    """
    pygame.draw.circle(window, color, (center[0], center[1]), RADIUS)
    # create a darker color and draw the outer circle of the disc
    darker = (int(color[0] * 0.7), int(color[1] * 0.7), int(color[2] * 0.7))
    pygame.draw.circle(window, darker, (center[0], center[1]), RADIUS, int(RADIUS / 4))


def draw_window(window: pygame.Surface, game: ConnectFour, buttons: list[Button]) -> None:
    """ Based on the given sqaure size, draw the whole interface on the given window at the current status of game
        If game.grid are all unoccupied, then just draw the window.
        game.grid record the bottom row first, top row last. Wherease on pygame, the location of top row has smallest
        y-value and the location of bottom row has greatest y-value. i.e. game.grid[y][x] == pygame's board [ROW_COLUMN - 1 - y][x]
    """
    window.fill(WHITE)
    grid = game.grid
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # four corners: c=0 r=0, c=COLUMN_COUNT-1 r=0,
            if c == 0 and r == 0:
                pygame.draw.rect(window, BLUE, ((c + 1) * SQUARESIZE, (r + 2) * SQUARESIZE, SQUARESIZE, SQUARESIZE), border_top_left_radius=BORDER_RADIUS)
            elif c == COLUMN_COUNT - 1 and r == 0:
                pygame.draw.rect(window, BLUE, ((c + 1) * SQUARESIZE, (r + 2) * SQUARESIZE, SQUARESIZE, SQUARESIZE), border_top_right_radius=BORDER_RADIUS)
            elif c == 0 and r == ROW_COUNT - 1:
                pygame.draw.rect(window, BLUE, ((c + 1) * SQUARESIZE, (r + 2) * SQUARESIZE, SQUARESIZE, SQUARESIZE), border_bottom_left_radius=BORDER_RADIUS)
            elif c == COLUMN_COUNT - 1 and r == ROW_COUNT - 1:
                pygame.draw.rect(window, BLUE, ((c + 1) * SQUARESIZE, (r + 2) * SQUARESIZE, SQUARESIZE, SQUARESIZE), border_bottom_right_radius=BORDER_RADIUS)
            else:
                pygame.draw.rect(window, BLUE, ((c + 1) * SQUARESIZE, (r + 2) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(window, WHITE, (
                int((c + 1) * SQUARESIZE + SQUARESIZE / 2), int((r + 2) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if grid[ROW_COUNT - 1 - r][c] == PLAYER_TWO:  # Player Two's disc
                center = (int((c + 1) * SQUARESIZE + SQUARESIZE / 2), int((r + 2) * SQUARESIZE + SQUARESIZE / 2))
                draw_one_disc(window, COLOR_PLAYER_TWO, center)
            elif grid[ROW_COUNT - 1 - r][c] == PLAYER_ONE:  # Player One's disc
                center = (int((c + 1) * SQUARESIZE + SQUARESIZE / 2), int((r + 2) * SQUARESIZE + SQUARESIZE / 2))
                draw_one_disc(window, COLOR_PLAYER_ONE, center)
    # draw the buttons:
    for button in buttons:
        if button.disabled is True:
            button.show_disabled(window)
        else:
            button.draw(window)
    # draw player one and its button and player two and its button
    draw_one_disc(window, COLOR_PLAYER_ONE, (SQUARESIZE * 3, (2 + COLUMN_COUNT) * SQUARESIZE))
    draw_one_disc(window, COLOR_PLAYER_TWO, (SQUARESIZE * 6, (2 + COLUMN_COUNT) * SQUARESIZE))

    text1 = FONT_WORDS.render('player one', True, BLACK)
    text2 = FONT_WORDS.render('player two', True, BLACK)
    window.blit(text1, (int(SQUARESIZE * 3 - SQUARESIZE / 2), int((2 + COLUMN_COUNT + 0.5) * SQUARESIZE)))
    window.blit(text2, (int(SQUARESIZE * 6 - SQUARESIZE / 2), int((2 + COLUMN_COUNT + 0.5) * SQUARESIZE)))
    pygame.display.update()

def print_win(screen: pygame.Surface, word: str) -> None:
    rec = pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0, int(WINDOW_HEIGHT / 2 - SQUARESIZE), WINDOW_WIDTH, SQUARESIZE), 2)
    # screen.fill((127, 255, 212), rec)
    screen.fill((min(int(BLUE[0] * 1.5), 255), min(int(BLUE[1] * 1.5), 255), min(int(BLUE[2] * 1.5), 255)), rec)

    text = FONT_WIN_STATUS.render(word, True, BLACK)
    text_rect = text.get_rect(center=(SIZE[0] / 2, SIZE[1] / 2 - SQUARESIZE/2))
    screen.blit(text, text_rect)

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

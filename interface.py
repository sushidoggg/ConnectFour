
from __future__ import annotations
from connect_four import ConnectFour
from main import SQAURESIZE, RADIUS, WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_PLAYER_ONE, COLOR_PLAYER_TWO, BLUE, WHITE, BLACK, ROW_COUNT, COLUMN_COUNT
import pygame

def draw_one_disc(window: pygame.Surface, color: tuple[int], center: tuple[int]) -> None:
    """Draw a beautiful disc on window at the given window with given color"""
    ...

def draw_window(window: pygame.Surface, game: ConnectFour) -> None:
    '''Based on the given sqaure size, draw the whole interface on the given window at the current status of game
        If game.grid are all unoccupied, then just draw the window'''
    window.fill(WHITE)
    pygame.display.flip()
    grid = game.grid
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(window, BLUE, ((c + 1)* SQUARESIZE, (r + 2) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(window, WHITE, (
                int((c + 1) * SQUARESIZE + SQUARESIZE / 2), int((r + 2) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if grid[r][c] == 1:  # Player Two's disc
                pygame.draw.circle(window, COLOR_PLAYER_TWO, (
                    int((c + 1) * SQUARESIZE + SQUARESIZE / 2), int((r + 2) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif grid[r][c] == 0:  # Player One's disc
                pygame.draw.circle(window, COLOR_PLAYER_ONE, (
                    int((c + 1) * SQUARESIZE + SQUARESIZE / 2), int((r + 2) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


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


def is_valid_position() -> bool:
# return the user's move as an integer to connect_four.py.
    ...

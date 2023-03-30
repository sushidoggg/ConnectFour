
from __future__ import annotations
from connect_four import ConnectFour
from main import SQAURESIZE, RADIUS, WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_PLAYER_ONE, COLOR_PLAYER_TWO, BLUE, WHITE, BLACK, ROW_COUNT, COLUMN_COUNT
import pygame

# todo: click the two buttons and see if it is user
class Button():
    """A class represents a circle buttons."""

    def __init__(self, x: int, y: int, image: str) -> None:
        """Create a button of given image at (x, y)"""
        self.image = image
        self.center = (x, y)
        self.clicked = False
    def draw(self, window: pygame.Surface) -> None:




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
            # TODO: convert grid-index to pygame's index
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

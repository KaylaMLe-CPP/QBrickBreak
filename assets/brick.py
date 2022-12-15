import pygame
from . import globals


class Brick(pygame.sprite.Sprite):
    def __init__(self, x_pos=0, y_pos=0):
        super().__init__()

        # creates and draws paddle on screen
        self.image = pygame.Surface(
            [globals.PADDLE_HEIGHT, globals.PADDLE_HEIGHT])
        self.image.fill(globals.WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos


class Qubricks:
    def __init__(self, x_pos) -> None:
        self.bricks = []
        # each state maps to a brick
        for i in range(2**globals.NUM_QUBITS):
            self.bricks.append(Brick(x_pos, i*globals.PADDLE_HEIGHT))
